import Profile from '../models/Profile.js';
import { generateBirthChart, getCompatibilityScore } from '../utils/astrology.js';

/**
 * Создание новой анкеты с расчётом натальной карты
 */
export const createProfile = async (req, res) => {
  try {
    const {
      name,
      birthDate,
      birthTime,
      lat = 55.7558,     // Москва по умолчанию
      lon = 37.6173,
      bio,
      gender,
      preferences,
      photoUrl,
    } = req.body;

    // Расчёт натальной карты
    const birthChart = await generateBirthChart(birthDate, birthTime, lat, lon);

    const newProfile = new Profile({
      name,
      bio,
      gender,
      preferences,
      birthDate,
      birthTime,
      location: { lat, lon },
      photoUrl,
      astrology: birthChart,
    });

    await newProfile.save();

    res.status(201).json({ message: 'Анкета успешно создана', profile: newProfile });
  } catch (err) {
    console.error('Ошибка при создании анкеты:', err);
    res.status(500).json({ error: 'Ошибка при создании анкеты' });
  }
};

/**
 * Получение списка совместимых анкет
 */
export const getCompatibleProfiles = async (req, res) => {
  try {
    const { userId } = req.params;

    const currentUser = await Profile.findById(userId);
    if (!currentUser) {
      return res.status(404).json({ error: 'Пользователь не найден' });
    }

    const allProfiles = await Profile.find({ _id: { $ne: userId } });

    const compatible = allProfiles
      .map((profile) => ({
        profile,
        score: getCompatibilityScore(currentUser.astrology, profile.astrology),
      }))
      .filter((entry) => entry.score >= 2) // фильтр: минимум 2 совпадения
      .sort((a, b) => b.score - a.score);

    res.json(compatible.map((entry) => entry.profile));
  } catch (err) {
    console.error('Ошибка при поиске совместимых анкет:', err);
    res.status(500).json({ error: 'Ошибка при поиске совместимых анкет' });
  }
};
