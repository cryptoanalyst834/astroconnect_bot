const Notification = require("../models/Notification");

exports.sendNotification = async (req, res) => {
  try {
    const { userId, message } = req.body;

    const notification = new Notification({ userId, message });
    await notification.save();

    res.status(201).json(notification);
  } catch (error) {
    console.error("Ошибка при отправке уведомления:", error);
    res.status(500).json({ message: "Ошибка при отправке уведомления" });
  }
};

exports.getNotifications = async (req, res) => {
  try {
    const { userId } = req.params;

    const notifications = await Notification.find({ userId }).sort({ createdAt: -1 });
    res.json(notifications);
  } catch (error) {
    console.error("Ошибка при получении уведомлений:", error);
    res.status(500).json({ message: "Ошибка получения уведомлений" });
  }
};
