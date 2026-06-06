// PROMPTARA — Constants & Initial State

export const STORAGE_KEY = 'promptara_v2';

export const INITIAL_DATA = {
  loggedInUserId: null,
  activeBoardId: null,
  users: [
    {
      id: 'hardcoded-admin',
      name: 'Admin Promptara',
      email: 'admin@promptara.id',
      password: 'admin',
      role: 'Owner',
      initials: 'AP',
      color: '#3EB8B8'
    }
  ],
  boards: [],
  columns: [
    { id: 'col1', name: 'Briefs',    color: '#6366F1', order: 0 },
    { id: 'col2', name: 'Studio',    color: '#F59E0B', order: 1 },
    { id: 'col3', name: 'Preview',   color: '#3B82F6', order: 2 },
    { id: 'col4', name: 'Touch Up',  color: '#EC4899', order: 3 },
    { id: 'col5', name: 'Done Deal', color: '#22C55E', order: 4 }
  ],
  cards: [],
  notifications: []
};

export const PROJECT_TYPES = {
  'web-design':     { label: 'Web Design',    color: '#2563EB', bg: '#EFF6FF' },
  'ui-ux':          { label: 'UI/UX',          color: '#8B5CF6', bg: '#F5F3FF' },
  'branding':       { label: 'Branding',       color: '#EC4899', bg: '#FDF2F8' },
  'product-design': { label: 'Product Design', color: '#F97316', bg: '#FFF7ED' },
  'social-media':   { label: 'Social Media',   color: '#14B8A6', bg: '#F0FDFA' },
  'other':          { label: 'Lainnya',         color: '#6B7280', bg: '#F3F4F6' }
};

export const PRIORITY = {
  high:   { label: 'Tinggi', color: '#EF4444', bg: '#FEF2F2' },
  medium: { label: 'Sedang', color: '#F59E0B', bg: '#FFFBEB' },
  low:    { label: 'Rendah', color: '#22C55E', bg: '#F0FDF4' }
};

export const ICON_PATHS = {
  board:    'M4 5a1 1 0 011-1h4a1 1 0 011 1v14a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v8a1 1 0 01-1 1h-4a1 1 0 01-1-1V5z',
  list:     'M4 6h16M4 10h16M4 14h10',
  chart:    'M3 3v18h18M7 16l4-4 4 4 4-8',
  bell:     'M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9',
  plus:     'M12 4v16m8-8H4',
  x:        'M6 18L18 6M6 6l12 12',
  check:    'M5 13l4 4L19 7',
  edit:     'M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z',
  trash:    'M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16',
  calendar: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z',
  user:     'M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z',
  users:    'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z',
  chat:     'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z',
  clip:     'M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13',
  download: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4',
  settings: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z M15 12a3 3 0 11-6 0 3 3 0 016 0z',
  logout:   'M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1',
  search:   'M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z',
  tag:      'M7 7h.01M7 3H5a2 2 0 00-2 2v2c0 .53.21 1.04.586 1.414l8 8a2 2 0 002.828 0l4-4a2 2 0 000-2.828l-8-8A2 2 0 007 3z',
  arrow:    'M9 5l7 7-7 7',
  eye:      'M15 12a3 3 0 11-6 0 3 3 0 016 0zM2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z',
  money:    'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z'
};
