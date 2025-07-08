const User = require("../models/User");
const VoiceMessage = require("../models/VoiceMessage");
const UsageLimit = require("../models/UsageLimit");

// Получить профиль пользователя
exports.getProfile = async (req, res) => {
  try {
    const user = await User.findById(req.params.id).lean();
    if (!user) return res.status(404).json({ message: "Пользователь не найден" });

    res.json(user);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Ошибка сервера" });
  }
};

// Обновить профиль
exports.updateProfile = async (req, res) => {
  try {
    const updates = req.body;
    const user = await User.findByIdAndUpdate(req.params.id, updates, { new: true }).lean();
    if (!user) return res.status(404).json({ message: "Пользователь не найден" });

    res.json(user);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Ошибка при обновлении профиля" });
  }
};

// Загрузить аудио
exports.uploadAudio = async (req, res) => {
  try {
    const { userId } = req.body;
    const file = req.file;

    if (!file) return res.status(400).json({ message: "Файл не найден" });

    const audioUrl = `/uploads/${file.filename}`;
    const audio = await VoiceMessage.create({
      userId,
      audioUrl,
      duration: req.body.duration || 0,
    });

    res.json(audio);
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Ошибка при загрузке аудио" });
  }
};
