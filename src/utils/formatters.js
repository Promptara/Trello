// PROMPTARA — Formatters & Date Helpers

export const formatIDR = (n) =>
  n == null ? '—' : 'Rp ' + Number(n).toLocaleString('id-ID');

export const formatDate = (s) => {
  if (!s) return '—';
  return new Date(s).toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
  });
};

export const formatDateShort = (s) => {
  if (!s) return '—';
  return new Date(s).toLocaleDateString('id-ID', {
    day: 'numeric',
    month: 'short',
  });
};

export const isOverdue = (s) =>
  s && new Date(s) < new Date(new Date().toDateString());

export const isDueSoon = (s) => {
  if (!s) return false;
  const diff = (new Date(s) - new Date()) / 86400000;
  return diff >= 0 && diff <= 3;
};
