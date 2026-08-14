import express from 'express';
import { getLabels, createLabel, deleteLabel } from '../controllers/labelsController.js';
import authMiddleware from '../middleware/authMiddleware.js';

const router = express.Router();

router.use(authMiddleware);

router.get('/', getLabels);
router.post('/', createLabel);
router.delete('/:id', deleteLabel);

export default router;
