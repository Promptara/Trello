// PROMPTARA — Card Detail / Edit Modal
import { useState, useContext } from 'react';
import { AppContext } from '../context/AppContext';
import { PROJECT_TYPES, PRIORITY } from '../constants';
import { genId } from '../utils/storage';
import { formatIDR, formatDate, isOverdue } from '../utils/formatters';
import Icon from './ui/Icon';
import TypeBadge from './ui/TypeBadge';
import PriorityPill from './ui/PriorityPill';
import Btn from './ui/Btn';
import Input from './ui/Input';
import Select from './ui/Select';

const CardModal = ({ cardId, defaultColumnId, onClose, isNew }) => {
  const { data, dispatch } = useContext(AppContext);
  const existing = cardId ? data.cards.find((c) => c.id === cardId) : null;

  const [title, setTitle] = useState(existing?.title || '');
  const [client, setClient] = useState(existing?.client || '');
  const [description, setDescription] = useState(existing?.description || '');
  const [type, setType] = useState(existing?.type || 'web-design');
  const [priority, setPriority] = useState(existing?.priority || 'medium');
  const [columnId, setColumnId] = useState(
    existing?.columnId || defaultColumnId || data.columns[0]?.id
  );
  const [dueDate, setDueDate] = useState(existing?.dueDate || '');
  const [value, setValue] = useState(
    existing?.value != null ? String(existing.value) : ''
  );
  const [dpPaid, setDpPaid] = useState(
    existing?.dpPaid != null ? String(existing.dpPaid) : ''
  );
  const [assignees, setAssignees] = useState(existing?.assignees || []);
  const [newComment, setNewComment] = useState('');
  const [activeTab, setActiveTab] = useState('detail');
  const [confirmDel, setConfirmDel] = useState(false);

  const currentUser = data.users.find((u) => u.id === data.loggedInUserId);

  const toggleAssignee = (uid) =>
    setAssignees((prev) =>
      prev.includes(uid) ? prev.filter((x) => x !== uid) : [...prev, uid]
    );

  // TODO: On save, call PATCH /api/cards/:id or POST /api/cards
  const handleSave = () => {
    if (!title.trim()) return;
    const cardData = {
      title: title.trim(),
      client: client.trim(),
      description: description.trim(),
      type,
      priority,
      columnId,
      dueDate,
      value: value ? Number(value) : 0,
      dpPaid: dpPaid ? Number(dpPaid) : 0,
      assignees,
    };
    if (isNew) {
      dispatch({
        type: 'ADD_CARD',
        card: {
          id: genId(),
          boardId: data.activeBoardId,
          order: 0,
          createdAt: new Date().toISOString(),
          comments: [],
          attachments: [],
          ...cardData,
        },
      });
    } else {
      dispatch({ type: 'UPDATE_CARD', cardId, updates: cardData });
    }
    onClose();
  };

  // TODO: Call DELETE /api/cards/:id
  const handleDelete = () => {
    dispatch({ type: 'DELETE_CARD', cardId });
    onClose();
  };

  // TODO: Call POST /api/cards/:id/comments
  const handleAddComment = () => {
    if (!newComment.trim() || !currentUser) return;
    dispatch({
      type: 'ADD_COMMENT',
      cardId,
      comment: {
        id: genId(),
        userId: currentUser.id,
        text: newComment.trim(),
        date: new Date().toISOString(),
      },
    });
    setNewComment('');
  };

  const TABS = [
    { id: 'detail', label: 'Detail' },
    {
      id: 'comments',
      label: `Komentar${
        existing?.comments?.length ? ` (${existing.comments.length})` : ''
      }`,
    },
    { id: 'attachments', label: 'Lampiran' },
  ];
  const outstanding = (Number(value) || 0) - (Number(dpPaid) || 0);

  return (
    <div>
      {/* Header */}
      <div className="p-[22px_24px_0] flex items-start gap-3">
        <div className="flex-1">
          <div className="flex gap-2 mb-2.5 flex-wrap">
            <TypeBadge type={type} />
            <PriorityPill priority={priority} />
            {!isNew && existing && isOverdue(existing.dueDate) && (
              <span className="text-[11px] font-semibold text-red-500 bg-red-50 py-[3px] px-[10px] rounded-full">
                Overdue
              </span>
            )}
          </div>
          <textarea
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Judul project..."
            className="w-full border-none outline-none resize-none text-[19px] font-bold text-ink bg-transparent leading-[1.35] p-0"
            style={{ fontFamily: 'inherit' }}
            rows={2}
          />
        </div>
        <button
          onClick={onClose}
          className="w-[34px] h-[34px] rounded-[9px] border-none cursor-pointer flex items-center justify-center shrink-0 mt-[2px] transition-colors"
          style={{ background: '#F0EFF8', color: '#5C5C7A' }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.background = '#E5E4EF')
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.background = '#F0EFF8')
          }
        >
          <Icon name="x" size={16} />
        </button>
      </div>

      {/* Sub-tabs */}
      {!isNew && (
        <div
          className="flex px-6 pt-[14px] mt-1 border-b"
          style={{ borderColor: '#F0EFF8' }}
        >
          {TABS.map((t) => (
            <button
              key={t.id}
              onClick={() => setActiveTab(t.id)}
              className="py-2 px-4 border-none bg-transparent cursor-pointer font-semibold text-[13px] transition-colors"
              style={{
                fontFamily: 'inherit',
                color: activeTab === t.id ? '#3EB8B8' : '#9090AA',
                borderBottom:
                  activeTab === t.id
                    ? '2px solid #3EB8B8'
                    : '2px solid transparent',
                marginBottom: -1.5,
              }}
            >
              {t.label}
            </button>
          ))}
        </div>
      )}

      <div className="p-[20px_24px_24px]">
        {/* DETAIL TAB */}
        {(isNew || activeTab === 'detail') && (
          <div className="flex flex-col gap-4">
            <div className="grid grid-cols-2 gap-3">
              <Select
                label="Tipe Project"
                value={type}
                onChange={(e) => setType(e.target.value)}
                options={Object.entries(PROJECT_TYPES).map(([k, v]) => ({
                  value: k,
                  label: v.label,
                }))}
              />
              <Select
                label="Prioritas"
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                options={Object.entries(PRIORITY).map(([k, v]) => ({
                  value: k,
                  label: v.label,
                }))}
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <Input
                label="Nama Klien"
                value={client}
                onChange={(e) => setClient(e.target.value)}
                placeholder="Nama perusahaan / klien"
              />
              <Select
                label="Status / Kolom"
                value={columnId}
                onChange={(e) => setColumnId(e.target.value)}
                options={(data.columns || []).map((c) => ({
                  value: c.id,
                  label: c.name,
                }))}
              />
            </div>

            <Input
              label="Deadline"
              type="date"
              value={dueDate}
              onChange={(e) => setDueDate(e.target.value)}
            />
            <Input
              label="Deskripsi"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Detail scope pekerjaan, catatan khusus, dll..."
              multiline
              rows={3}
            />

            {/* Financial */}
            <div className="bg-surface rounded-xl p-[14px_16px]">
              <p
                className="m-0 mb-3 text-xs font-bold tracking-[0.4px] uppercase"
                style={{ color: '#5C5C7A' }}
              >
                Detail Keuangan
              </p>
              <div className="grid grid-cols-2 gap-3">
                <Input
                  label="Nilai Project (IDR)"
                  type="number"
                  value={value}
                  onChange={(e) => setValue(e.target.value)}
                  placeholder="0"
                />
                <Input
                  label="DP Diterima (IDR)"
                  type="number"
                  value={dpPaid}
                  onChange={(e) => setDpPaid(e.target.value)}
                  placeholder="0"
                />
              </div>
              {Number(value) > 0 && (
                <div className="flex gap-4 mt-3 p-[10px_12px] bg-white rounded-[9px] border border-line">
                  <div className="flex-1">
                    <div
                      className="text-[10px] font-semibold mb-[2px]"
                      style={{ color: '#9090AA' }}
                    >
                      TOTAL
                    </div>
                    <div className="text-[13px] font-bold text-ink">
                      {formatIDR(Number(value))}
                    </div>
                  </div>
                  <div className="flex-1">
                    <div
                      className="text-[10px] font-semibold mb-[2px]"
                      style={{ color: '#22C55E' }}
                    >
                      DITERIMA
                    </div>
                    <div
                      className="text-[13px] font-bold"
                      style={{ color: '#22C55E' }}
                    >
                      {formatIDR(Number(dpPaid) || 0)}
                    </div>
                  </div>
                  <div className="flex-1">
                    <div
                      className="text-[10px] font-semibold mb-[2px]"
                      style={{
                        color: outstanding > 0 ? '#F59E0B' : '#9090AA',
                      }}
                    >
                      SISA
                    </div>
                    <div
                      className="text-[13px] font-bold"
                      style={{
                        color: outstanding > 0 ? '#F59E0B' : '#9090AA',
                      }}
                    >
                      {formatIDR(outstanding)}
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Assignees */}
            <div>
              <label
                className="block text-xs font-bold tracking-[0.4px] uppercase mb-2"
                style={{ color: '#5C5C7A' }}
              >
                Tim Pengerjaan
              </label>
              <div className="flex flex-wrap gap-2">
                {(data.users || []).map((u) => {
                  const active = assignees.includes(u.id);
                  return (
                    <button
                      key={u.id}
                      onClick={() => toggleAssignee(u.id)}
                      className="flex items-center gap-2 py-[7px] px-3 rounded-[10px] cursor-pointer transition-all"
                      style={{
                        border: `1.5px solid ${
                          active ? u.color : '#E5E4EF'
                        }`,
                        background: active ? u.color + '18' : '#fff',
                        fontFamily: 'inherit',
                      }}
                    >
                      <div
                        className="w-[22px] h-[22px] rounded-full flex items-center justify-center text-[9px] font-bold text-white"
                        style={{ background: u.color }}
                      >
                        {u.initials}
                      </div>
                      <span
                        className="text-xs font-semibold"
                        style={{
                          color: active ? '#17172E' : '#5C5C7A',
                        }}
                      >
                        {u.name}
                      </span>
                      {active && (
                        <Icon
                          name="check"
                          size={12}
                          color={u.color}
                          strokeWidth={2.5}
                        />
                      )}
                    </button>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* COMMENTS TAB */}
        {!isNew && activeTab === 'comments' && (
          <div className="flex flex-col gap-3.5">
            {(existing?.comments || []).length === 0 && (
              <div
                className="text-center py-6 text-[13px]"
                style={{ color: '#9090AA' }}
              >
                Belum ada komentar. Jadilah yang pertama!
              </div>
            )}
            {(existing?.comments || []).map((cm) => {
              const u = data.users.find((x) => x.id === cm.userId);
              return (
                <div key={cm.id} className="flex gap-2.5">
                  {u && (
                    <div
                      className="w-8 h-8 rounded-full flex items-center justify-center text-[11px] font-bold text-white shrink-0"
                      style={{ background: u.color }}
                    >
                      {u.initials}
                    </div>
                  )}
                  <div className="flex-1">
                    <div className="flex gap-2 items-baseline mb-1">
                      <span className="text-xs font-bold text-ink">
                        {u?.name || 'Unknown'}
                      </span>
                      <span
                        className="text-[11px]"
                        style={{ color: '#9090AA' }}
                      >
                        {formatDate(cm.date)}
                      </span>
                    </div>
                    <div className="bg-surface rounded-[10px] p-[10px_12px] text-[13px] text-ink leading-[1.5]">
                      {cm.text}
                    </div>
                  </div>
                </div>
              );
            })}
            {currentUser && (
              <div
                className="flex gap-2.5 mt-1 pt-3.5 border-t"
                style={{ borderColor: '#F0EFF8' }}
              >
                <div
                  className="w-8 h-8 rounded-full flex items-center justify-center text-[11px] font-bold text-white shrink-0"
                  style={{ background: currentUser.color }}
                >
                  {currentUser.initials}
                </div>
                <div className="flex-1 flex gap-2">
                  <textarea
                    value={newComment}
                    onChange={(e) => setNewComment(e.target.value)}
                    placeholder="Tulis komentar..."
                    rows={2}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        handleAddComment();
                      }
                    }}
                    className="flex-1 border border-line rounded-[10px] p-[8px_12px] text-[13px] text-ink resize-none outline-none bg-[#FAFAF8]"
                    style={{ fontFamily: 'inherit' }}
                  />
                  <Btn
                    onClick={handleAddComment}
                    small
                    disabled={!newComment.trim()}
                  >
                    Kirim
                  </Btn>
                </div>
              </div>
            )}
          </div>
        )}

        {/* ATTACHMENTS TAB */}
        {!isNew && activeTab === 'attachments' && (
          <div className="flex flex-col gap-2.5">
            {(existing?.attachments || []).map((a) => (
              <div
                key={a.id}
                className="flex items-center gap-2.5 bg-surface rounded-[10px] p-[10px_14px] border border-line"
              >
                <Icon name="clip" size={16} color="#9090AA" />
                <span className="flex-1 text-[13px] font-semibold text-ink">
                  {a.name}
                </span>
                <span className="text-[11px]" style={{ color: '#9090AA' }}>
                  {a.size}
                </span>
              </div>
            ))}
            <div
              className="border-2 border-dashed border-line rounded-xl p-6 text-center cursor-pointer transition-colors"
              style={{ color: '#9090AA' }}
              onMouseEnter={(e) =>
                (e.currentTarget.style.borderColor = '#3EB8B8')
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.borderColor = '#E5E4EF')
              }
            >
              <Icon name="clip" size={22} color="#9090AA" />
              <p className="mt-2 mb-0 text-[13px] font-semibold">
                Drag & drop file atau klik untuk upload
              </p>
              <p className="mt-1 mb-0 text-[11px]">
                PDF, PNG, JPG, FIG, AI (maks. 50MB)
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div
        className="px-6 py-4 border-t flex justify-between items-center"
        style={{ borderColor: '#F0EFF8' }}
      >
        <div>
          {!isNew &&
            (confirmDel ? (
              <div className="flex gap-2 items-center">
                <span className="text-xs font-semibold text-red-500">
                  Yakin hapus?
                </span>
                <Btn onClick={handleDelete} small danger>
                  Ya, hapus
                </Btn>
                <Btn
                  onClick={() => setConfirmDel(false)}
                  small
                  variant="ghost"
                >
                  Batal
                </Btn>
              </div>
            ) : (
              <Btn
                onClick={() => setConfirmDel(true)}
                small
                variant="ghost"
                style={{ color: '#EF4444' }}
              >
                <Icon name="trash" size={14} color="#EF4444" /> Hapus
              </Btn>
            ))}
        </div>
        <div className="flex gap-2">
          <Btn onClick={onClose} variant="secondary">
            Batal
          </Btn>
          <Btn onClick={handleSave} disabled={!title.trim()}>
            <Icon name="check" size={14} color="#fff" strokeWidth={2.5} />
            {isNew ? 'Buat Card' : 'Simpan'}
          </Btn>
        </div>
      </div>
    </div>
  );
};

export default CardModal;
