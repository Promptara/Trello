// PROMPTARA — Sidebar, NotifPanel, AddBoardForm
import { useState, useContext, useRef, useEffect } from 'react';
import { AppContext } from '../context/AppContext';
import { genId } from '../utils/storage';
import { formatDate } from '../utils/formatters';
import Icon from './ui/Icon';

/* ── Notification Panel ─────────────────────────────── */
const NotifPanel = () => {
  const { data, dispatch } = useContext(AppContext);
  const notifs = [...(data.notifications || [])].sort(
    (a, b) => new Date(b.date) - new Date(a.date)
  );
  const TYPE_ICON = {
    'due-soon': 'calendar',
    comment: 'chat',
    assignment: 'user',
  };
  const TYPE_COLOR = {
    'due-soon': '#F59E0B',
    comment: '#3EB8B8',
    assignment: '#22C55E',
  };

  return (
    <div
      className="bg-white rounded-[14px] overflow-hidden"
      style={{
        width: 300,
        border: '1.5px solid #E5E4EF',
        boxShadow: '0 12px 40px rgba(0,0,0,0.14)',
      }}
    >
      <div
        className="flex justify-between items-center px-4 py-[14px] border-b"
        style={{ borderColor: '#F0EFF8' }}
      >
        <span className="text-[13px] font-bold text-ink">Notifikasi</span>
        <button
          onClick={() => dispatch({ type: 'MARK_ALL_READ' })}
          className="bg-transparent border-none cursor-pointer text-[11px] font-semibold p-0 text-brand"
        >
          Semua dibaca
        </button>
      </div>
      <div className="overflow-y-auto" style={{ maxHeight: 300 }}>
        {notifs.length === 0 && (
          <div
            className="py-7 px-4 text-center text-xs"
            style={{ color: '#9090AA' }}
          >
            Tidak ada notifikasi.
          </div>
        )}
        {notifs.map((n) => (
          <div
            key={n.id}
            onClick={() => dispatch({ type: 'MARK_NOTIF_READ', id: n.id })}
            className="flex gap-2.5 items-start px-4 py-[11px] cursor-pointer transition-colors border-b"
            style={{
              background: n.read ? '#fff' : '#F8F7FF',
              borderColor: '#F7F6F3',
            }}
            onMouseEnter={(e) =>
              (e.currentTarget.style.background = '#F0EFF8')
            }
            onMouseLeave={(e) =>
              (e.currentTarget.style.background = n.read
                ? '#fff'
                : '#F8F7FF')
            }
          >
            <div
              className="w-7 h-7 rounded-lg shrink-0 flex items-center justify-center"
              style={{
                background:
                  (TYPE_COLOR[n.type] || '#9090AA') + '15',
              }}
            >
              <Icon
                name={TYPE_ICON[n.type] || 'bell'}
                size={13}
                color={TYPE_COLOR[n.type] || '#9090AA'}
              />
            </div>
            <div className="flex-1 min-w-0">
              <div
                className="text-xs text-ink leading-[1.45] mb-[2px]"
                style={{ fontWeight: n.read ? 500 : 700 }}
              >
                {n.message}
              </div>
              <div
                className="text-[10px] font-medium"
                style={{ color: '#B0AFBF' }}
              >
                {formatDate(n.date)}
              </div>
            </div>
            {!n.read && (
              <div className="w-[6px] h-[6px] rounded-full shrink-0 mt-[5px] bg-brand" />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

/* ── Add Board Inline Form ──────────────────────────── */
const AddBoardForm = ({ onAdd, onCancel }) => {
  const [name, setName] = useState('');
  const inputRef = useRef(null);

  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (name.trim()) onAdd(name.trim());
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-1 mt-1 px-2">
      <input
        ref={inputRef}
        value={name}
        onChange={(e) => setName(e.target.value)}
        onKeyDown={(e) => e.key === 'Escape' && onCancel()}
        placeholder="Nama board..."
        className="flex-1 text-xs border border-line rounded-lg px-2 py-1.5 outline-none bg-surface text-ink min-w-0"
        style={{ fontFamily: 'inherit' }}
      />
      <button
        type="submit"
        disabled={!name.trim()}
        className="text-xs font-semibold px-2 py-1 rounded-md border-none cursor-pointer transition-colors disabled:opacity-40"
        style={{
          background: '#3EB8B8',
          color: '#fff',
          fontFamily: 'inherit',
        }}
      >
        OK
      </button>
      <button
        type="button"
        onClick={onCancel}
        className="text-xs font-semibold px-2 py-1 rounded-md border-none cursor-pointer"
        style={{
          background: '#F0EFF8',
          color: '#5C5C7A',
          fontFamily: 'inherit',
        }}
      >
        ✕
      </button>
    </form>
  );
};

/* ── Sidebar ────────────────────────────────────────── */
const Sidebar = ({ view, setView, currentUser, unread }) => {
  const { data, dispatch } = useContext(AppContext);
  const [notifOpen, setNotifOpen] = useState(false);
  const [addingBoard, setAddingBoard] = useState(false);
  const notifBtnRef = useRef(null);
  const [notifPos, setNotifPos] = useState({ top: 0, left: 0 });
  const isOwner = currentUser?.role === 'Owner';

  const NAV = [
    { id: 'board', icon: 'board', label: 'Board' },
    { id: 'calendar', icon: 'calendar', label: 'Timeline' },
    { id: 'orders', icon: 'list', label: 'Riwayat Order' },
    { id: 'finance', icon: 'chart', label: 'Keuangan' },
    { id: 'team', icon: 'users', label: 'Tim' },
  ];

  const openNotif = () => {
    if (notifBtnRef.current) {
      const rect = notifBtnRef.current.getBoundingClientRect();
      setNotifPos({ top: rect.top, left: rect.right + 8 });
    }
    setNotifOpen((o) => !o);
  };

  const handleAddBoard = (name) => {
    dispatch({
      type: 'ADD_BOARD',
      board: {
        id: genId(),
        name,
        client: '',
        color: '#3EB8B8',
        createdAt: new Date().toISOString(),
      },
    });
    setAddingBoard(false);
  };

  return (
    <div
      className="flex flex-col h-screen shrink-0"
      style={{
        width: 216,
        background: '#fff',
        borderRight: '1.5px solid #ECEAF4',
      }}
    >
      {/* Logo */}
      <div
        className="px-4 py-[14px] border-b"
        style={{ borderColor: '#F0EFF8' }}
      >
        <img src="/logo.png" alt="PROMPTARA.AI" className="h-8 block" />
      </div>

      {/* Nav */}
      <nav className="py-1.5 flex-1 overflow-y-auto">
        {/* Boards section */}
        <div className="px-4 pt-2 pb-1">
          <div className="flex items-center justify-between mb-1">
            <span
              className="text-[9px] font-bold tracking-[1.2px] uppercase"
              style={{ color: '#C0BFCF' }}
            >
              Boards
            </span>
            {isOwner && (
              <button
                onClick={() => setAddingBoard(true)}
                className="bg-transparent border-none cursor-pointer p-[2px] rounded transition-colors"
                style={{ color: '#B0AFBF', lineHeight: 1 }}
                onMouseEnter={(e) =>
                  (e.currentTarget.style.color = '#3EB8B8')
                }
                onMouseLeave={(e) =>
                  (e.currentTarget.style.color = '#B0AFBF')
                }
                title="Tambah board"
              >
                <Icon name="plus" size={12} strokeWidth={2.5} />
              </button>
            )}
          </div>

          {(data.boards || []).map((b) => {
            const active = data.activeBoardId === b.id;
            const bCards = (data.cards || []).filter(
              (c) => c.boardId === b.id
            );
            return (
              <button
                key={b.id}
                onClick={() => {
                  dispatch({ type: 'SET_BOARD', boardId: b.id });
                  setView('board');
                }}
                className="w-full flex items-center gap-[7px] border-none cursor-pointer text-xs transition-all mb-[1px]"
                style={{
                  padding: '7px 8px 7px 9px',
                  fontFamily: 'inherit',
                  borderLeft: `3px solid ${
                    active ? b.color : 'transparent'
                  }`,
                  background: active ? b.color + '12' : 'transparent',
                  color: active ? '#17172E' : '#6B6B88',
                  fontWeight: active ? 700 : 500,
                  borderRadius: 0,
                }}
              >
                <div
                  className="w-[7px] h-[7px] rounded-full shrink-0"
                  style={{ background: b.color }}
                />
                <span className="flex-1 overflow-hidden text-ellipsis whitespace-nowrap text-left">
                  {b.name}
                </span>
                <span
                  className="text-[9px] font-bold"
                  style={{
                    color: active ? b.color : '#C0BFCF',
                  }}
                >
                  {bCards.length}
                </span>
              </button>
            );
          })}

          {addingBoard && (
            <AddBoardForm
              onAdd={handleAddBoard}
              onCancel={() => setAddingBoard(false)}
            />
          )}
        </div>

        <div
          className="h-px my-1.5"
          style={{ background: '#F0EFF8' }}
        />

        {/* Nav items */}
        {NAV.map((n) => {
          const active = view === n.id;
          return (
            <button
              key={n.id}
              onClick={() => setView(n.id)}
              className="w-full flex items-center gap-[9px] border-none cursor-pointer text-[13px] transition-all mb-[1px]"
              style={{
                padding: '9px 16px 9px 17px',
                fontFamily: 'inherit',
                borderLeft: `3px solid ${
                  active ? '#3EB8B8' : 'transparent'
                }`,
                background: active
                  ? 'rgba(62,184,184,0.07)'
                  : 'transparent',
                color: active ? '#3EB8B8' : '#6B6B88',
                fontWeight: active ? 700 : 500,
                borderRadius: 0,
              }}
              onMouseEnter={(e) => {
                if (!active) {
                  e.currentTarget.style.background = '#F5F4FA';
                  e.currentTarget.style.color = '#17172E';
                }
              }}
              onMouseLeave={(e) => {
                if (!active) {
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.color = '#6B6B88';
                }
              }}
            >
              <Icon
                name={n.icon}
                size={15}
                color={active ? '#3EB8B8' : '#ADADC4'}
              />
              {n.label}
            </button>
          );
        })}
      </nav>

      {/* Notification bell */}
      <div className="pt-1">
        <button
          ref={notifBtnRef}
          onClick={openNotif}
          className="w-full flex items-center gap-[9px] border-none cursor-pointer text-[13px] font-medium transition-all"
          style={{
            padding: '9px 16px 9px 17px',
            fontFamily: 'inherit',
            borderLeft: `3px solid ${
              notifOpen ? '#3EB8B8' : 'transparent'
            }`,
            background: notifOpen
              ? 'rgba(62,184,184,0.07)'
              : 'transparent',
            color: notifOpen ? '#3EB8B8' : '#6B6B88',
            borderRadius: 0,
          }}
          onMouseEnter={(e) => {
            if (!notifOpen) {
              e.currentTarget.style.background = '#F5F4FA';
              e.currentTarget.style.color = '#17172E';
            }
          }}
          onMouseLeave={(e) => {
            if (!notifOpen) {
              e.currentTarget.style.background = 'transparent';
              e.currentTarget.style.color = '#6B6B88';
            }
          }}
        >
          <div className="relative shrink-0">
            <Icon
              name="bell"
              size={15}
              color={notifOpen ? '#3EB8B8' : '#ADADC4'}
            />
            {unread > 0 && (
              <div
                className="absolute flex items-center justify-center text-white font-extrabold rounded-full"
                style={{
                  top: -3,
                  right: -4,
                  width: 13,
                  height: 13,
                  fontSize: 7,
                  background: '#EF4444',
                  border: '1.5px solid #fff',
                }}
              >
                {unread}
              </div>
            )}
          </div>
          Notifikasi
        </button>
      </div>

      {/* User footer */}
      <div
        className="p-3 pb-3.5 mt-1 border-t"
        style={{ borderColor: '#F0EFF8' }}
      >
        <div className="flex items-center gap-[9px] p-2 rounded-[9px] bg-surface">
          <div
            className="w-7 h-7 rounded-full flex items-center justify-center text-[10px] font-extrabold text-white shrink-0"
            style={{ background: currentUser?.color }}
          >
            {currentUser?.initials}
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-xs font-bold text-ink overflow-hidden text-ellipsis whitespace-nowrap">
              {currentUser?.name}
            </div>
            <div
              className="text-[10px] font-medium"
              style={{ color: '#9090AA' }}
            >
              {currentUser?.role}
            </div>
          </div>
          <button
            onClick={() => dispatch({ type: 'LOGOUT' })}
            title="Keluar"
            className="bg-transparent border-none cursor-pointer p-1 rounded-md transition-all"
            style={{ color: '#C0BFCF' }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = '#EF4444';
              e.currentTarget.style.background = '#FEF2F2';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = '#C0BFCF';
              e.currentTarget.style.background = 'transparent';
            }}
          >
            <Icon name="logout" size={13} />
          </button>
        </div>
      </div>

      {/* Notification panel (fixed portal) */}
      {notifOpen && (
        <>
          <div
            className="fixed inset-0"
            style={{ zIndex: 190 }}
            onClick={() => setNotifOpen(false)}
          />
          <div
            className="fixed"
            style={{
              top: notifPos.top,
              left: notifPos.left,
              zIndex: 200,
            }}
          >
            <NotifPanel />
          </div>
        </>
      )}
    </div>
  );
};

export default Sidebar;
