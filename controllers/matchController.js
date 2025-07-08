const User = require("../models/User");
const Match = require("../models/Match");

exports.getRecommendedProfiles = async (req, res) => {
  try {
    const { userId } = req.query;

    const currentUser = await User.findById(userId);
    if (!currentUser) return res.status(404).json({ message: "Пользователь не найден" });

    const recommendations = await User.find({
      _id: { $ne: userId },
      gender: currentUser.interestedIn,
      age: { $gte: currentUser.ageRange[0], $lte: currentUser.ageRange[1] },
    }).limit(20);

    res.json(recommendations);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Ошибка подбора анкет" });
  }
};
