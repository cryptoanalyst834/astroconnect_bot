import BirthChart from '../models/birthChart.model.js';
import { generateBirthChart } from '../utils/astrology.js';

export const createBirthChart = async (req, res) => {
  try {
    const { userId, birthDate, birthTime, birthPlace } = req.body;

    const chartData = await generateBirthChart(birthDate, birthTime, birthPlace);
    
    const chart = new BirthChart({
      userId,
      birthDate,
      birthTime,
      birthPlace,
      ...chartData
    });

    await chart.save();
    res.status(201).json(chart);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'Failed to create chart' });
  }
};
