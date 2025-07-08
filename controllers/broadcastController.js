const Notification = require("../models/Notification");
const User = require("../models/User");

exports.broadcastMessage = async (req, res) => {
  try {
    const { message } = req.body;

    const users = await User.find({});
    const notifications = users.map((user) => ({
      userId: user._id,
      message,
    }));

    await Notification.insertMany(notifications);
    res.status(200).json({ sent: notifications.length });
  } catch (error) {
    console.error("Ошибка при рассылке:", error);
    res.status(500).json({ message: "Ошибка при рассылке" });
  }
};
