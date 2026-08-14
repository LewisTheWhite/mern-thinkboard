import Note from '../models/Note.js';

function parseLocalDateBoundary(value, endOfDay = false) {
    const [year, month, day] = value.split('-').map(Number);

    if (endOfDay) {
        return new Date(year, month - 1, day, 23, 59, 59, 999);
    }

    return new Date(year, month - 1, day, 0, 0, 0, 0);
}

export async function getAllNotes(req, res){
    try {
        const { title, labels, dateFrom, dateTo } = req.query;
        const filter = { userId: req.user.id };

        if (title) {
            filter.title = { $regex: title, $options: 'i' };
        }

        if (labels) {
            const labelIds = labels.split(',').filter(Boolean);
            if (labelIds.length > 0) {
                filter.labels = { $in: labelIds };
            }
        }

        if (dateFrom || dateTo) {
            filter.createdAt = {};
            if (dateFrom) {
                filter.createdAt.$gte = parseLocalDateBoundary(dateFrom);
            }
            if (dateTo) {
                filter.createdAt.$lte = parseLocalDateBoundary(dateTo, true);
            }
        }

        const notes = await Note.find(filter).populate('labels').sort({ createdAt: -1 });
        res.status(200).json(notes);
    } catch (error) {
        console.error('Error fetching notes:', error);
        res.status(500).json({ message: "Internal Server error" });
    }
}

export async function getNoteById(req, res){
    try {
        const note = await Note.findOne({ _id: req.params.id, userId: req.user.id }).populate('labels'); // Fetch the note only if it belongs to the current user
        if (!note) {
            return res.status(404).json({ message: "Note not found" }); // If the note with the given ID does not exist, return a 404 error
        }
        res.status(200).json(note);
    } catch (error) {
        console.error('Error fetching note by ID:', error);
        res.status(500).json({ message: "Internal Server error" });
    }
}

export async function createNote(req, res){
    try {
        const { title, content, labels } = req.body;
        const note = new Note({
            userId: req.user.id,
            title,
            content,
            labels: Array.isArray(labels) ? labels : [],
        });

        const savedNote = await note.save(); // Save the new note to the database
        res.status(201).json(savedNote);
        
    } catch (error) {
        console.error('Error creating note:', error);
        res.status(500).json({ message: "Internal Server error" });
    }
}

export async function updateNote(req, res){
    try {
        const { title, content, labels } = req.body;
        const updateData = { title, content };
        if (Array.isArray(labels)) {
            updateData.labels = labels;
        }
        const updatedNote = await Note.findOneAndUpdate(
            { _id: req.params.id, userId: req.user.id },
            updateData,
            { new: true }
        ); // Update only if the note belongs to the current user
        if (!updatedNote) {
            return res.status(404).json({ message: "Note not found" }); // If the note with the given ID does not exist, return a 404 error
        }

        res.status(200).json(updatedNote);
    } catch (error) {
        console.error('Error updating note:', error);
        res.status(500).json({ message: "Internal Server error" });
    }
}

export async function deleteNote(req, res){
    try {
        const deletedNote = await Note.findOneAndDelete({ _id: req.params.id, userId: req.user.id }); // Delete only if the note belongs to the current user
        if (!deletedNote) {
            return res.status(404).json({ message: "Note not found" }); // If the note with the given ID does not exist, return a 404 error
        }
        res.status(200).json({"message": "Note deleted successfully!"});
    } catch (error) {
        console.error('Error in deleteNote controller:', error);
        res.status(500).json({ message: "Internal Server error" });
    }
}
