import mongoose from 'mongoose';

const labelSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      default: null, // null = system default label
    },
    name: {
      type: String,
      required: true,
      trim: true,
    },
    color: {
      type: String,
      required: true,
      match: /^#[0-9a-fA-F]{6}$/,
    },
    isDefault: {
      type: Boolean,
      default: false,
    },
  },
  { timestamps: true }
);

// Unique label name per user (null userId = system defaults)
labelSchema.index({ userId: 1, name: 1 }, { unique: true });

const Label = mongoose.model('Label', labelSchema);

export default Label;
