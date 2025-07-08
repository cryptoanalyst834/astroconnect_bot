import express from 'express';
import { createBirthChart } from '../controllers/birthChart.controller.js';
const router = express.Router();

router.post('/', createBirthChart);

export default router;
