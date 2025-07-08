import { generateBirthChart, getCompatibilityScore } from '../utils/astrology.js';

router.post('/birthchart', async (req, res) => {
  const { date, time, lat, lon } = req.body;
  try {
    const chart = await generateBirthChart(date, time, lat, lon);
    res.json(chart);
  } catch (err) {
    res.status(500).json({ error: 'Ошибка при генерации карты' });
  }
});

router.post('/compatibility', async (req, res) => {
  const { user1, user2 } = req.body;
  try {
    const score = getCompatibilityScore(user1, user2);
    res.json({ score });
  } catch (err) {
    res.status(500).json({ error: 'Ошибка при расчёте совместимости' });
  }
});
