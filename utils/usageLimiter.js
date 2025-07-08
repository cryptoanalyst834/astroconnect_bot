const UsageLimit = require('../models/UsageLimit');

exports.checkDailyLimit = async (userId, limit = 10) => {
  const record = await UsageLimit.findOne({ user: userId });
  const today = new Date();

  if (!record) {
    await UsageLimit.create({ user: userId, dailyLikes: 1 });
    return true;
  }

  const diff = (today - new Date(record.lastReset)) / 1000 / 60 / 60;
  if (diff > 24) {
    record.dailyLikes = 1;
    record.lastReset = today;
    await record.save();
    return true;
  }

  if (record.dailyLikes >= limit) return false;

  record.dailyLikes += 1;
  await record.save();
  return true;
};
