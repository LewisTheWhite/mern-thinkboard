import Label from '../models/Label.js';
import Note from '../models/Note.js';

export async function getLabels(req, res) {
  try {
    // Return system defaults + user's custom labels
    const labels = await Label.find({
      $or: [{ userId: null, isDefault: true }, { userId: req.user.id }],
    }).sort({ isDefault: -1, name: 1 });

    return res.status(200).json(labels);
  } catch (error) {
    console.error('Error fetching labels:', error);
    return res.status(500).json({ message: 'Internal Server error' });
  }
}

export async function createLabel(req, res) {
  try {
    const { name, color } = req.body;

    if (!name?.trim()) {
      return res.status(400).json({ message: 'Label name is required' });
    }

    if (name.trim().length > 25) {
      return res.status(400).json({ message: 'Label name must be 25 characters or fewer' });
    }

    if (!color || !/^#[0-9a-fA-F]{6}$/.test(color)) {
      return res.status(400).json({ message: 'Valid hex color is required (e.g. #ff5500)' });
    }

    // Check for duplicate name for this user (including system defaults)
    const existing = await Label.findOne({
      $or: [
        { userId: req.user.id, name: name.trim() },
        { userId: null, name: name.trim() },
      ],
    });

    if (existing) {
      return res.status(409).json({ message: 'A label with this name already exists' });
    }

    const label = await Label.create({
      userId: req.user.id,
      name: name.trim(),
      color,
      isDefault: false,
    });

    return res.status(201).json(label);
  } catch (error) {
    console.error('Error creating label:', error);
    return res.status(500).json({ message: 'Internal Server error' });
  }
}

export async function deleteLabel(req, res) {
  try {
    const label = await Label.findById(req.params.id);

    if (!label) {
      return res.status(404).json({ message: 'Label not found' });
    }

    // Prevent deleting system defaults
    if (label.isDefault) {
      return res.status(403).json({ message: 'Cannot delete a default label' });
    }

    // Only owner can delete their label
    if (label.userId?.toString() !== req.user.id) {
      return res.status(403).json({ message: 'Not authorized to delete this label' });
    }

    // Remove this label from all user's notes
    await Note.updateMany(
      { userId: req.user.id, labels: label._id },
      { $pull: { labels: label._id } }
    );

    await Label.findByIdAndDelete(req.params.id);

    return res.status(200).json({ message: 'Label deleted successfully' });
  } catch (error) {
    console.error('Error deleting label:', error);
    return res.status(500).json({ message: 'Internal Server error' });
  }
}
