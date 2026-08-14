import Label from '../models/Label.js';

const DEFAULT_LABELS = [
  { name: 'Work', color: '#3b82f6' },
  { name: 'Personal', color: '#8b5cf6' },
  { name: 'Ideas', color: '#f59e0b' },
  { name: 'Urgent', color: '#ef4444' },
  { name: 'Archive', color: '#6b7280' },
];

export async function seedDefaultLabels() {
  const existingCount = await Label.countDocuments({ userId: null, isDefault: true });

  if (existingCount >= DEFAULT_LABELS.length) {
    return; // Already seeded
  }

  for (const label of DEFAULT_LABELS) {
    await Label.findOneAndUpdate(
      { userId: null, name: label.name },
      { ...label, userId: null, isDefault: true },
      { upsert: true, new: true }
    );
  }

  console.log('[Seed] Default labels created');
}
