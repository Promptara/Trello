// PROMPTARA — Calendar & Gantt Timeline View
import { useState, useContext, useRef, useEffect } from 'react';
import { AppContext } from '../context/AppContext';
import { formatDate, formatDateShort } from '../utils/formatters';
import Icon from '../components/ui/Icon';
import Modal from '../components/ui/Modal';
import CardModal from '../components/CardModal';

/* ── Gantt Timeline ──────────────────────────────────── */
const GanttTimeline = ({ cards }) => {
  const { data } = useContext(AppContext);
  const [openCardId, setOpenCardId] = useState(null);
  const scrollRef = useRef(null);

  const allDates = cards
    .flatMap((c) => [c.createdAt, c.dueDate].filter(Boolean))
    .map((d) => new Date(d));
  if (allDates.length === 0)
    return (
      <div
        className="flex-1 flex items-center justify-center text-[13px]"
        style={{ color: '#B0AFBF' }}
      >
        Belum ada project dengan tanggal. Tambahkan deadline di card!
      </div>
    );

  const minDate = new Date(Math.min(...allDates));
  const maxDate = new Date(Math.max(...allDates));
  minDate.setDate(minDate.getDate() - 10);
  maxDate.setDate(maxDate.getDate() + 14);

  const totalDays = Math.max(
    1,
    Math.ceil((maxDate - minDate) / 86400000)
  );
  const DAY_W = Math.max(
    20,
    Math.min(38, Math.floor(1100 / totalDays))
  );
  const LEFT_W = 230;
  const ROW_H = 44;
  const HEADER_H = 36;

  const toX = (date) => {
    if (!date) return null;
    return Math.ceil((new Date(date) - minDate) / 86400000) * DAY_W;
  };

  const todayX = toX(new Date());

  const monthMarkers = [];
  const cur = new Date(minDate);
  cur.setDate(1);
  while (cur <= maxDate) {
    monthMarkers.push({
      label: cur.toLocaleDateString('id-ID', {
        month: 'short',
        year: '2-digit',
      }),
      x: toX(cur),
    });
    cur.setMonth(cur.getMonth() + 1);
  }

  const weekLines = [];
  const wc = new Date(minDate);
  while (wc <= maxDate) {
    weekLines.push(toX(wc));
    wc.setDate(wc.getDate() + 7);
  }

  const sorted = [...cards].sort(
    (a, b) => new Date(a.createdAt || 0) - new Date(b.createdAt || 0)
  );

  useEffect(() => {
    if (scrollRef.current && todayX !== null) {
      scrollRef.current.scrollLeft = Math.max(
        0,
        LEFT_W + todayX - 300
      );
    }
  }, []);

  const totalW = LEFT_W + totalDays * DAY_W + 40;

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Legend */}
      <div className="px-5 py-2 flex gap-4 flex-wrap shrink-0">
        {(data.columns || []).map((col) => (
          <div key={col.id} className="flex items-center gap-[5px]">
            <div
              className="w-2.5 h-2.5 rounded-[2px]"
              style={{ background: col.color }}
            />
            <span
              className="text-[11px] font-semibold"
              style={{ color: '#9090AA' }}
            >
              {col.name}
            </span>
          </div>
        ))}
        <div className="flex items-center gap-[5px] ml-auto">
          <div
            className="w-2.5 h-[2px]"
            style={{ background: '#EF4444', opacity: 0.7 }}
          />
          <span
            className="text-[11px] font-semibold"
            style={{ color: '#9090AA' }}
          >
            Hari ini
          </span>
        </div>
      </div>

      {/* Scrollable grid */}
      <div ref={scrollRef} className="flex-1 overflow-auto relative">
        <div style={{ width: totalW, position: 'relative' }}>
          {/* Sticky header */}
          <div
            className="sticky top-0 z-10 flex bg-white"
            style={{
              borderBottom: '2px solid #ECEAF4',
              height: HEADER_H,
            }}
          >
            <div
              className="shrink-0 flex items-center px-4 text-[10px] font-bold uppercase tracking-[0.5px]"
              style={{
                width: LEFT_W,
                borderRight: '1px solid #ECEAF4',
                color: '#B0AFBF',
              }}
            >
              Project
            </div>
            <div className="flex-1 relative">
              {monthMarkers.map((m, i) => (
                <div
                  key={i}
                  className="absolute top-0 h-full flex items-center pl-2"
                  style={{ left: m.x }}
                >
                  <span
                    className="text-[11px] font-bold uppercase tracking-[0.3px] whitespace-nowrap"
                    style={{ color: '#6B6B88' }}
                  >
                    {m.label}
                  </span>
                </div>
              ))}
              {weekLines.map((x, i) => (
                <div
                  key={i}
                  className="absolute top-0 bottom-0 w-px"
                  style={{ left: x, background: '#F0EFF8' }}
                />
              ))}
              {todayX !== null && (
                <div
                  className="absolute top-[2px] bottom-[2px] w-[2px] rounded-sm"
                  style={{
                    left: todayX,
                    background: '#EF4444',
                    opacity: 0.7,
                  }}
                />
              )}
            </div>
          </div>

          {/* Card rows */}
          {sorted.map((card, i) => {
            const col = (data.columns || []).find(
              (c) => c.id === card.columnId
            );
            const color = col?.color || '#9090AA';
            const startX = card.createdAt ? toX(card.createdAt) : 0;
            const endX = card.dueDate
              ? toX(card.dueDate)
              : startX + DAY_W * 14;
            const barW = Math.max(endX - startX, DAY_W * 2);
            const done = card.columnId === 'col5';
            const over =
              !done &&
              card.dueDate &&
              new Date(card.dueDate) < new Date();
            const barColor = over ? '#EF4444' : color;
            const paidPct =
              card.value > 0
                ? Math.min(100, (card.dpPaid / card.value) * 100)
                : 0;

            return (
              <div
                key={card.id}
                className="gantt-row flex items-center cursor-pointer transition-colors"
                onClick={() => setOpenCardId(card.id)}
                style={{
                  height: ROW_H,
                  background: i % 2 === 0 ? '#fff' : '#FAFAF8',
                  borderBottom: '1px solid #F5F4FA',
                }}
              >
                {/* Name column */}
                <div
                  className="shrink-0 px-3.5 flex items-center gap-2"
                  style={{
                    width: LEFT_W,
                    borderRight: '1px solid #ECEAF4',
                  }}
                >
                  <div
                    className="w-1.5 h-1.5 rounded-full shrink-0"
                    style={{ background: color }}
                  />
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-bold text-ink overflow-hidden text-ellipsis whitespace-nowrap">
                      {card.title}
                    </div>
                    {card.client && (
                      <div
                        className="text-[10px] font-medium mt-[1px]"
                        style={{ color: '#B0AFBF' }}
                      >
                        {card.client}
                      </div>
                    )}
                  </div>
                </div>

                {/* Bar area */}
                <div className="flex-1 relative h-full">
                  {weekLines.map((x, wi) => (
                    <div
                      key={wi}
                      className="absolute top-0 bottom-0 w-px pointer-events-none"
                      style={{ left: x, background: '#F5F4FA' }}
                    />
                  ))}
                  {todayX !== null && (
                    <div
                      className="absolute top-0 bottom-0 w-[2px] pointer-events-none"
                      style={{
                        left: todayX,
                        background: 'rgba(239,68,68,0.35)',
                        zIndex: 2,
                      }}
                    />
                  )}

                  {/* Main bar */}
                  <div
                    className="absolute rounded-[5px] overflow-hidden"
                    style={{
                      left: startX,
                      top: '50%',
                      transform: 'translateY(-50%)',
                      width: barW,
                      height: 22,
                      background: barColor,
                      opacity: done ? 0.35 : 0.88,
                      zIndex: 1,
                    }}
                    title={`${card.title} | ${formatDate(card.createdAt)} → ${formatDate(card.dueDate)}`}
                  >
                    {paidPct > 0 && (
                      <div
                        className="absolute left-0 top-0 bottom-0 rounded-l-[5px]"
                        style={{
                          width: `${paidPct}%`,
                          background: 'rgba(255,255,255,0.25)',
                        }}
                      />
                    )}
                    {barW > 80 && (
                      <span
                        className="absolute left-2 top-1/2 -translate-y-1/2 text-[10px] font-bold text-white whitespace-nowrap"
                        style={{
                          textShadow: '0 1px 2px rgba(0,0,0,0.2)',
                        }}
                      >
                        {card.client || card.title}
                      </span>
                    )}
                  </div>

                  {/* Due date diamond marker */}
                  {endX !== null && (
                    <div
                      className="absolute rounded-[2px]"
                      style={{
                        left: startX + barW - 6,
                        top: '50%',
                        transform: 'translateY(-50%) rotate(45deg)',
                        width: 9,
                        height: 9,
                        background: over ? '#EF4444' : barColor,
                        border: '2px solid #fff',
                        zIndex: 3,
                      }}
                      title={`Deadline: ${formatDate(card.dueDate)}`}
                    />
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

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
    </div>
  );
};

/* ── Month Calendar ───────────────────────────────────── */
const MonthCalendar = ({ cards }) => {
  const { data } = useContext(AppContext);
  const [viewDate, setViewDate] = useState(new Date());
  const [openCardId, setOpenCardId] = useState(null);

  const yr = viewDate.getFullYear(),
    mo = viewDate.getMonth();
  const firstDow = (new Date(yr, mo, 1).getDay() + 6) % 7;
  const daysInMo = new Date(yr, mo + 1, 0).getDate();
  const totalCells = Math.ceil((firstDow + daysInMo) / 7) * 7;

  const byDay = {};
  for (const c of cards) {
    if (!c.dueDate) continue;
    const d = new Date(c.dueDate);
    if (d.getFullYear() === yr && d.getMonth() === mo) {
      const k = d.getDate();
      (byDay[k] = byDay[k] || []).push(c);
    }
  }

  const today = new Date();
  const isToday = (day) =>
    today.getFullYear() === yr &&
    today.getMonth() === mo &&
    today.getDate() === day;

  const navBtnClass =
    'w-[30px] h-[30px] rounded-lg bg-white cursor-pointer flex items-center justify-center';
  const navBtnStyle = {
    border: '1.5px solid #E5E4EF',
    fontFamily: 'inherit',
  };

  return (
    <div className="flex-1 overflow-auto p-[16px_24px_24px]">
      {/* Month nav */}
      <div className="flex items-center gap-3 mb-[18px]">
        <button
          onClick={() => setViewDate(new Date(yr, mo - 1))}
          className={navBtnClass}
          style={navBtnStyle}
        >
          <Icon
            name="arrow"
            size={14}
            color="#9090AA"
            style={{ transform: 'rotate(180deg)' }}
          />
        </button>
        <span className="text-base font-extrabold text-ink tracking-[-0.3px]">
          {viewDate.toLocaleDateString('id-ID', {
            month: 'long',
            year: 'numeric',
          })}
        </span>
        <button
          onClick={() => setViewDate(new Date(yr, mo + 1))}
          className={navBtnClass}
          style={navBtnStyle}
        >
          <Icon name="arrow" size={14} color="#9090AA" />
        </button>
        <button
          onClick={() => setViewDate(new Date())}
          className="ml-auto py-[5px] px-3.5 rounded-lg bg-white text-xs font-semibold cursor-pointer"
          style={{
            border: '1.5px solid #E5E4EF',
            color: '#5C5C7A',
            fontFamily: 'inherit',
          }}
        >
          Hari ini
        </button>
      </div>

      {/* Day headers */}
      <div className="grid grid-cols-7 gap-1 mb-1">
        {['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'].map(
          (d) => (
            <div
              key={d}
              className="text-center text-[10px] font-bold uppercase tracking-[0.5px] py-1"
              style={{ color: '#B0AFBF' }}
            >
              {d}
            </div>
          )
        )}
      </div>

      {/* Calendar grid */}
      <div className="grid grid-cols-7 gap-1">
        {Array.from({ length: totalCells }, (_, i) => {
          const day = i - firstDow + 1;
          const valid = day >= 1 && day <= daysInMo;
          const dayCards = valid ? byDay[day] || [] : [];
          const tod = valid && isToday(day);
          return (
            <div
              key={i}
              className="cal-day rounded-[9px] p-1.5 transition-colors"
              style={{
                minHeight: 80,
                background: tod
                  ? '#E8F7F7'
                  : valid
                    ? '#fff'
                    : '#FAFAF8',
                border: `1.5px solid ${tod ? '#3EB8B8' : '#E5E4EF'}`,
                opacity: valid ? 1 : 0.35,
                cursor:
                  dayCards.length > 0 ? 'pointer' : 'default',
              }}
            >
              {valid && (
                <>
                  <div
                    className="text-xs mb-[5px]"
                    style={{
                      fontWeight: tod ? 800 : 600,
                      color: tod ? '#3EB8B8' : '#17172E',
                    }}
                  >
                    {day}
                  </div>
                  {dayCards.slice(0, 3).map((c) => {
                    const col = (data.columns || []).find(
                      (x) => x.id === c.columnId
                    );
                    return (
                      <div
                        key={c.id}
                        onClick={() => setOpenCardId(c.id)}
                        className="text-[10px] font-semibold py-[2px] px-1.5 rounded mb-[2px] overflow-hidden text-ellipsis whitespace-nowrap cursor-pointer transition-opacity hover:opacity-75"
                        style={{
                          background:
                            (col?.color || '#9090AA') + '22',
                          color: col?.color || '#9090AA',
                        }}
                        title={c.title}
                      >
                        {c.title}
                      </div>
                    );
                  })}
                  {dayCards.length > 3 && (
                    <div
                      className="text-[9px] font-bold"
                      style={{ color: '#B0AFBF' }}
                    >
                      +{dayCards.length - 3} lagi
                    </div>
                  )}
                </>
              )}
            </div>
          );
        })}
      </div>

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
    </div>
  );
};

/* ── Calendar View (main) ────────────────────────────── */
const CalendarView = () => {
  const { data } = useContext(AppContext);
  const [sub, setSub] = useState('gantt');
  const activeBoard = data.activeBoardId;
  const cards = (data.cards || []).filter(
    (c) => !activeBoard || c.boardId === activeBoard
  );

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* Header */}
      <div
        className="px-5 pt-4 pb-3 border-b bg-white shrink-0"
        style={{ borderColor: '#E5E4EF' }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h2 className="m-0 text-[17px] font-extrabold text-ink tracking-[-0.4px]">
              Timeline & Kalender
            </h2>
            <p
              className="m-0 mt-[2px] text-[11px]"
              style={{ color: '#B0AFBF' }}
            >
              Read-only · untuk edit card, gunakan Board view
            </p>
          </div>
          {/* Sub-tab switcher */}
          <div className="flex bg-surface rounded-[10px] p-[3px] gap-[2px]">
            {[
              ['gantt', 'Timeline'],
              ['calendar', 'Kalender'],
            ].map(([id, label]) => (
              <button
                key={id}
                onClick={() => setSub(id)}
                className="py-[7px] px-[18px] border-none rounded-lg cursor-pointer font-semibold text-xs transition-all"
                style={{
                  fontFamily: 'inherit',
                  background: sub === id ? '#fff' : 'transparent',
                  color: sub === id ? '#17172E' : '#9090AA',
                  boxShadow:
                    sub === id
                      ? '0 1px 4px rgba(0,0,0,0.08)'
                      : 'none',
                }}
              >
                {label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {sub === 'gantt' ? (
        <GanttTimeline cards={cards} />
      ) : (
        <MonthCalendar cards={cards} />
      )}
    </div>
  );
};

export default CalendarView;
