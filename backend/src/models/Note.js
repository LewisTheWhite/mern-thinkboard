import mongoose from 'mongoose';

const noteSchema = new mongoose.Schema(
    {
        userId: {
            type: mongoose.Schema.Types.ObjectId,
            ref: 'User',
            required: true
        },
        title: {
            type: String,
            required: true
        },
        content: {
            type: String,
            required: true
        },
        labels: [{
            type: mongoose.Schema.Types.ObjectId,
            ref: 'Label'
        }],
    }, 
    { timestamps: true } // Automatically adds createdAt and updatedAt fields
);

const Note = mongoose.model('Note', noteSchema);

export default Note;