const { Chart, Ephemeris, DateTime, Observer } = require('flatlib');
const ephem = Ephemeris.full();

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

function getCompatibilityScore(user1, user2) {
  let score = 0;
  if (compatibleSigns[user1.sun]?.includes(user2.sun)) score++;
  if (compatibleSigns[user1.venus]?.includes(user2.venus)) score++;
  if (user1.ascendant === user2.moon) score++;

  return score;
}

module.exports = { getCompatibilityScore };
