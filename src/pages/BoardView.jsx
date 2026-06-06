// PROMPTARA — Kanban Board View
import { useState, useContext } from 'react';
import { AppContext } from '../context/AppContext';
import { PROJECT_TYPES, PRIORITY } from '../constants';
import { formatIDR, formatDateShort, isOverdue, isDueSoon } from '../utils/formatters';
import Icon from '../components/common/ui/Icon';
import TypeBadge from '../components/common/ui/TypeBadge';
import Avatar from '../components/common/ui/Avatar';
import Btn from '../components/common/ui/Btn';
import Modal from '../components/common/ui/Modal';
import CardModal from '../components/features/CardModal';

/* ── Single Card ─────────────────────────────────────── */
const BoardCard = ({ card, onOpen, onDragStart, onDragEnd }) => {
  const [hov, setHov] = useState(false);
  const pColor = (PRIORITY[card.priority] || PRIORITY.low).color;
  const overdue = isOverdue(card.dueDate);
  const dueSoon = !overdue && isDueSoon(card.dueDate);

  return (
    <div
      draggable
      onDragStart={(e) => {
        e.dataTransfer.effectAllowed = 'move';
        onDragStart(card.id);
      }}
      onDragEnd={onDragEnd}
      onClick={() => onOpen(card.id)}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      className="bg-white rounded-[11px] p-[12px_14px] cursor-pointer select-none"
      style={{
        border: `1.5px solid ${hov ? '#C7C6D8' : '#E5E4EF'}`,
        borderLeft: `3.5px solid ${pColor}`,
        transition: 'box-shadow .15s, border-color .15s, transform .12s',
        boxShadow: hov
          ? '0 4px 14px rgba(0,0,0,0.1)'
          : '0 1px 3px rgba(0,0,0,0.05)',
        transform: hov ? 'translateY(-1px)' : 'none',
      }}
    >
      {/* Top row: type badge + value */}
      <div className="flex justify-between items-start mb-[7px] gap-1.5">
        <TypeBadge type={card.type} small />
        {card.value > 0 && (
          <span
            className="text-[10px] font-bold whitespace-nowrap"
            style={{ color: '#9090AA' }}
          >
            {formatIDR(card.value).replace('Rp ', 'Rp')}
          </span>
        )}
      </div>

      {/* Title */}
      <div
        className="text-[13px] font-bold text-ink leading-[1.4] mb-1.5 overflow-hidden"
        style={{
          display: '-webkit-box',
          WebkitLineClamp: 2,
          WebkitBoxOrient: 'vertical',
        }}
      >
        {card.title}
      </div>

      {/* Client */}
      {card.client && (
        <div
          className="text-[11px] font-medium mb-2 overflow-hidden text-ellipsis whitespace-nowrap"
          style={{ color: '#9090AA' }}
        >
          {card.client}
        </div>
      )}

      {/* Bottom row */}
      <div className="flex items-center justify-between mt-1 gap-1.5">
        {card.dueDate ? (
          <span
            className="text-[10px] font-semibold rounded-[7px] py-[3px] px-[7px] flex items-center gap-[3px]"
            style={{
              background: overdue
                ? '#FEF2F2'
                : dueSoon
                  ? '#FFFBEB'
                  : '#F7F6F3',
              color: overdue
                ? '#EF4444'
                : dueSoon
                  ? '#F59E0B'
                  : '#9090AA',
            }}
          >
            <Icon
              name="calendar"
              size={9}
              color={
                overdue ? '#EF4444' : dueSoon ? '#F59E0B' : '#9090AA'
              }
              strokeWidth={2}
            />
            {formatDateShort(card.dueDate)}
          </span>
        ) : (
          <span />
        )}

        {/* Assignees */}
        <div className="flex flex-row-reverse">
          {(card.assignees || []).slice(0, 4).map((uid, i) => (
            <div key={uid} style={{ marginLeft: i === 0 ? 0 : -7 }}>
              <Avatar userId={uid} size={22} showRing />
            </div>
          ))}
          {card.assignees?.length > 4 && (
            <div
              className="flex items-center justify-center text-[9px] font-bold rounded-full"
              style={{
                width: 22,
                height: 22,
                background: '#E5E4EF',
                color: '#5C5C7A',
                border: '2px solid white',
                marginLeft: -7,
              }}
            >
              +{card.assignees.length - 4}
            </div>
          )}
        </div>
      </div>

      {/* DP progress bar */}
      {card.value > 0 && (
        <div className="mt-2">
          <div
            className="h-[3px] rounded-full overflow-hidden"
            style={{ background: '#F0EFF8' }}
          >
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: `${Math.min(100, Math.round((card.dpPaid / card.value) * 100))}%`,
                background:
                  card.dpPaid >= card.value ? '#22C55E' : '#3EB8B8',
              }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

/* ── Column ──────────────────────────────────────────── */
const BoardColumn = ({
  column,
  cards,
  onOpenCard,
  onAddCard,
  onDrop,
  dragOverCol,
  setDragOverCol,
}) => {
  const isOver = dragOverCol === column.id;

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setDragOverCol(column.id);
      }}
      onDragLeave={(e) => {
        if (!e.currentTarget.contains(e.relatedTarget))
          setDragOverCol(null);
      }}
      onDrop={(e) => {
        e.preventDefault();
        onDrop(column.id);
        setDragOverCol(null);
      }}
      className="flex flex-col rounded-[14px] p-[12px_10px] flex-shrink-0 transition-all"
      style={{
        width: 272,
        background: isOver ? '#E8E6F4' : '#EDECF4',
        border: isOver
          ? `2px solid ${column.color}`
          : '2px solid transparent',
        maxHeight: 'calc(100vh - 120px)',
      }}
    >
      {/* Column header */}
      <div className="flex items-center gap-[7px] mb-2.5 px-1 py-[2px]">
        <div
          className="w-[9px] h-[9px] rounded-full shrink-0"
          style={{ background: column.color }}
        />
        <span className="text-[13px] font-bold text-ink flex-1 tracking-[-0.1px]">
          {column.name}
        </span>
        <span
          className="text-[11px] font-bold px-2 py-[2px] rounded-full"
          style={{
            color: column.color,
            background: column.color + '20',
          }}
        >
          {cards.length}
        </span>
        <button
          onClick={() => onAddCard(column.id)}
          className="w-[26px] h-[26px] border-none rounded-[7px] bg-transparent cursor-pointer flex items-center justify-center transition-all"
          style={{ color: '#9090AA' }}
          onMouseEnter={(e) => {
            e.currentTarget.style.background = column.color + '25';
            e.currentTarget.style.color = column.color;
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.background = 'transparent';
            e.currentTarget.style.color = '#9090AA';
          }}
        >
          <Icon name="plus" size={15} strokeWidth={2.2} />
        </button>
      </div>

      {/* Cards list */}
      <div
        className="flex flex-col gap-[7px] overflow-y-auto flex-1 pr-[2px]"
        style={{
          scrollbarWidth: 'thin',
          scrollbarColor: '#D4D3E0 transparent',
        }}
      >
        {cards.map((card) => (
          <BoardCard
            key={card.id}
            card={card}
            onOpen={onOpenCard}
            onDragStart={(id) => (window.__dragging = id)}
            onDragEnd={() => {}}
          />
        ))}
      </div>

      {/* Add card footer */}
      <button
        onClick={() => onAddCard(column.id)}
        className="mt-2 w-full py-2 rounded-[9px] bg-transparent cursor-pointer text-xs font-semibold flex items-center justify-center gap-[5px] transition-all"
        style={{
          border: '1.5px dashed #C7C6D8',
          color: '#9090AA',
          fontFamily: 'inherit',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.borderColor = column.color;
          e.currentTarget.style.color = column.color;
          e.currentTarget.style.background = column.color + '0D';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.borderColor = '#C7C6D8';
          e.currentTarget.style.color = '#9090AA';
          e.currentTarget.style.background = 'transparent';
        }}
      >
        <Icon name="plus" size={13} strokeWidth={2.2} /> Tambah card
      </button>
    </div>
  );
};

/* ── Board View ──────────────────────────────────────── */
const BoardView = () => {
  const { data, dispatch } = useContext(AppContext);
  const [openCardId, setOpenCardId] = useState(null);
  const [newCardColId, setNewCardColId] = useState(null);
  const [dragOverCol, setDragOverCol] = useState(null);
  const [searchQ, setSearchQ] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterPriority, setFilterPriority] = useState('all');

  const cols = [...(data.columns || [])].sort((a, b) => a.order - b.order);
  const activeBoard = data.activeBoardId;
  const board = (data.boards || []).find((b) => b.id === activeBoard);

  const filteredCards = (data.cards || []).filter((c) => {
    if (!activeBoard || c.boardId !== activeBoard) return false;
    const q = searchQ.toLowerCase();
    const matchQ =
      !q ||
      c.title.toLowerCase().includes(q) ||
      (c.client || '').toLowerCase().includes(q);
    const matchT = filterType === 'all' || c.type === filterType;
    const matchP =
      filterPriority === 'all' || c.priority === filterPriority;
    return matchQ && matchT && matchP;
  });

  const getColCards = (colId) =>
    filteredCards
      .filter((c) => c.columnId === colId)
      .sort((a, b) => a.order - b.order);

  const handleDrop = (targetColId) => {
    const cardId = window.__dragging;
    if (cardId) {
      dispatch({
        type: 'UPDATE_CARD',
        cardId,
        updates: { columnId: targetColId },
      });
      window.__dragging = null;
    }
    setDragOverCol(null);
  };

  const totalValue = filteredCards.reduce(
    (s, c) => s + (c.value || 0),
    0
  );
  const totalDone = filteredCards.filter(
    (c) => c.columnId === 'col5'
  ).length;

  if (!board) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-3 text-center px-8">
        <Icon name="board" size={40} color="#D4D3E0" />
        <p
          className="text-sm font-semibold"
          style={{ color: '#9090AA' }}
        >
          Pilih atau buat board baru dari sidebar.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full overflow-hidden">
      {/* Board toolbar */}
      <div
        className="flex items-center gap-2.5 px-5 py-4 border-b bg-white shrink-0"
        style={{ borderColor: '#E5E4EF' }}
      >
        <div className="flex-1">
          <h2 className="m-0 text-[17px] font-extrabold text-ink tracking-[-0.4px]">
            {board.name}
          </h2>
          <p
            className="m-0 text-[11px] mt-[1px]"
            style={{ color: '#B0AFBF' }}
          >
            {filteredCards.length} cards · {totalDone} selesai ·{' '}
            {formatIDR(totalValue)}
          </p>
        </div>

        {/* Search */}
        <div className="relative">
          <div className="absolute left-[9px] top-1/2 -translate-y-1/2 pointer-events-none">
            <Icon name="search" size={13} color="#ADADC4" />
          </div>
          <input
            value={searchQ}
            onChange={(e) => setSearchQ(e.target.value)}
            placeholder="Cari project..."
            className="border border-line rounded-[9px] py-[7px] pl-[30px] pr-2.5 text-xs text-ink outline-none bg-surface"
            style={{ width: 170, fontFamily: 'inherit' }}
          />
        </div>

        {/* Filters */}
        <select
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="border border-line rounded-[9px] py-[7px] px-2.5 text-xs text-[#5C5C7A] bg-surface outline-none cursor-pointer"
          style={{ fontFamily: 'inherit' }}
        >
          <option value="all">Semua Tipe</option>
          {Object.entries(PROJECT_TYPES).map(([k, v]) => (
            <option key={k} value={k}>
              {v.label}
            </option>
          ))}
        </select>

        <select
          value={filterPriority}
          onChange={(e) => setFilterPriority(e.target.value)}
          className="border border-line rounded-[9px] py-[7px] px-2.5 text-xs text-[#5C5C7A] bg-surface outline-none cursor-pointer"
          style={{ fontFamily: 'inherit' }}
        >
          <option value="all">Semua Prioritas</option>
          {Object.entries(PRIORITY).map(([k, v]) => (
            <option key={k} value={k}>
              {v.label}
            </option>
          ))}
        </select>

        <Btn onClick={() => setNewCardColId(cols[0]?.id)} small>
          <Icon name="plus" size={13} color="#fff" strokeWidth={2.5} />{' '}
          Tambah
        </Btn>
      </div>

      {/* Columns */}
      <div
        className="flex-1 overflow-x-auto overflow-y-hidden p-[18px_20px] flex gap-3 items-start"
        style={{
          scrollbarWidth: 'thin',
          scrollbarColor: '#D4D3E0 transparent',
        }}
      >
        {cols.map((col) => (
          <BoardColumn
            key={col.id}
            column={col}
            cards={getColCards(col.id)}
            onOpenCard={(id) => setOpenCardId(id)}
            onAddCard={(colId) => setNewCardColId(colId)}
            onDrop={handleDrop}
            dragOverCol={dragOverCol}
            setDragOverCol={setDragOverCol}
          />
        ))}
      </div>

      {/* Card detail modal */}
      <Modal
        open={!!openCardId}
        onClose={() => setOpenCardId(null)}
        width={580}
      >
        {openCardId && (
          <CardModal
            cardId={openCardId}
            onClose={() => setOpenCardId(null)}
          />
        )}
      </Modal>

      {/* New card modal */}
      <Modal
        open={!!newCardColId}
        onClose={() => setNewCardColId(null)}
        width={580}
      >
        {newCardColId && (
          <CardModal
            defaultColumnId={newCardColId}
            isNew
            onClose={() => setNewCardColId(null)}
          />
        )}
      </Modal>
    </div>
  );
};

export default BoardView;
