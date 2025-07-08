const UsageLimit = require("../models/UsageLimit");

exports.incrementUsage = async (req, res) => {
  try {
    const { userId, feature } = req.body;

    let record = await UsageLimit.findOne({ userId });
    if (!record) {
      record = new UsageLimit({ userId, limits: { [feature]: 1 } });
    } else {
      record.limits[feature] = (record.limits[feature] || 0) + 1;
    }

    await record.save();
    res.status(200).json(record);
  } catch (error) {
    console.error("Ошибка при обновлении лимита:", error);
    res.status(500).json({ message: "Ошибка обновления лимита" });
  }
};

exports.getLimits = async (req, res) => {
  try {
    const { userId } = req.params;
    const limits = await UsageLimit.findOne({ userId });

    res.json(limits || {});
  } catch (error) {
    console.error("Ошибка при получении лимитов:", error);
    res.status(500).json({ message: "Ошибка получения лимитов" });
  }
};
