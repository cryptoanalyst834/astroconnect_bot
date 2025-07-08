import { Chart, DateTime, Observer } from 'flatlib';
import { ephemeris as eph } from 'flatlib/ephem';

// Координаты по умолчанию — Москва
const DEFAULT_LAT = 55.7558;
const DEFAULT_LON = 37.6173;

const compatibleSigns = {
  Aries: ['Leo', 'Sagittarius', 'Gemini', 'Aquarius'],
  Taurus: ['Virgo', 'Capricorn', 'Cancer', 'Pisces'],
  Gemini: ['Libra', 'Aquarius', 'Aries', 'Leo'],
  Cancer: ['Scorpio', 'Pisces', 'Taurus', 'Virgo'],
  Leo: ['Aries', 'Sagittarius', 'Gemini', 'Libra'],
  Virgo: ['Taurus', 'Capricorn', 'Cancer', 'Scorpio'],
  Libra: ['Gemini', 'Aquarius', 'Leo', 'Sagittarius'],
  Scorpio: ['Cancer', 'Pisces', 'Virgo', 'Capricorn'],
  Sagittarius: ['Aries', 'Leo', 'Libra', 'Aquarius'],
  Capricorn: ['Taurus', 'Virgo', 'Scorpio', 'Pisces'],
  Aquarius: ['Gemini', 'Libra', 'Aries', 'Sagittarius'],
  Pisces: ['Cancer', 'Scorpio', 'Taurus', 'Capricorn']
};

/**
 * Генерирует натальную карту по дате, времени и месту рождения
 */
export async function generateBirthChart(date, time, lat = DEFAULT_LAT, lon = DEFAULT_LON) {
  try {
    const datetime = new DateTime(`${date} ${time}`);
    const observer = new Observer(lat, lon);

    const chart = new Chart(datetime, observer, eph);

    return {
      sun: chart.get('SUN').sign,
      moon: chart.get('MOON').sign,
      venus: chart.get('VEN').sign,
      ascendant: chart.ASC.sign,
    };
  } catch (err) {
    console.error('Ошибка при расчёте карты:', err);
    throw new Error('Ошибка расчёта натальной карты');
  }
}

/**
 * Расчёт совместимости на основе Солнца, Венеры и Луны/Асцендента
 */
export function getCompatibilityScore(user1, user2) {
  let score = 0;

  if (compatibleSigns[user1.sun]?.includes(user2.sun)) score++;
  if (compatibleSigns[user1.venus]?.includes(user2.venus)) score++;
  if (user1.ascendant === user2.moon) score++;

  return score; // максимум — 3
}
