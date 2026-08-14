import express from 'express';
import dotenv from 'dotenv';
import cors from 'cors';

import notesRoutes from './routes/notesRoutes.js';
import authRoutes from './routes/authRoutes.js';
import labelsRoutes from './routes/labelsRoutes.js';
import rateLimiter from './middleware/rateLimiter.js';
import { connectDB } from './config/db.js';
import { seedDefaultLabels } from './seeds/defaultLabels.js';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5001;

// Middleware
app.use(cors({
    origin:"http://localhost:5173"
  }
)); // Enable CORS for all routes

app.use(express.json()); // To parse JSON bodies
app.use(rateLimiter); // Apply the rate limiter middleware to all routes

app.use('/api/auth', authRoutes);
app.use("/api/notes", notesRoutes);
app.use('/api/labels', labelsRoutes);

connectDB().then(async () => {
  await seedDefaultLabels();
  app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
  });
})


