// TODO: dynamically fetch
const types = ['CFR', 'High-speed', 'International', 'Night train'],
  days = ['All', 'Weekdays', 'Weekends'];
const isInt = (val) => typeof val === 'number' || /^\d+$/.test(val);

exports.isValidDay = (day) => days.includes(day);
exports.isValidType = (type) => types.includes(type);
exports.isValidHour = (hour) => isInt(hour) && hour >= 0 && hour <= 24;
exports.isValidEmail = (email) => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(email);
