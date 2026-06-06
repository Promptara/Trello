// PROMPTARA — Orders / Project History View
import { useState, useContext } from 'react';
import { AppContext } from '../context/AppContext';
import { PROJECT_TYPES } from '../constants';
import { formatIDR, formatDate, formatDateShort, isOverdue } from '../utils/formatters';
import Icon from '../components/ui/Icon';
import TypeBadge from '../components/ui/TypeBadge';
import Avatar from '../components/ui/Avatar';
import Btn from '../components/ui/Btn';
import Modal from '../components/ui/Modal';
import CardModal from '../components/CardModal';

const OrdersView = () => {
  const { data } = useContext(AppContext);
  const [search, setSearch] = useState('');
  const [filterType, setFilterType] = useState('all');
  const [filterCol, setFilterCol] = useState('all');
  const [sortBy, setSortBy] = useState('date-desc');
  const [addOpen, setAddOpen] = useState(false);
  const [editId, setEditId] = useState(null);

  const orders = (data.cards || []).filter((c) => {
    const q = search.toLowerCase();
    const matchQ =
      !q ||
      c.title.toLowerCase().includes(q) ||
      (c.client || '').toLowerCase().includes(q);
    const matchT = filterType === 'all' || c.type === filterType;
    const matchC = filterCol === 'all' || c.columnId === filterCol;
    return matchQ && matchT && matchC;
  });

  const sorted = [...orders].sort((a, b) => {
    if (sortBy === 'date-desc')
      return new Date(b.createdAt) - new Date(a.createdAt);
    if (sortBy === 'date-asc')
      return new Date(a.createdAt) - new Date(b.createdAt);
    if (sortBy === 'value-desc') return (b.value || 0) - (a.value || 0);
    if (sortBy === 'value-asc') return (a.value || 0) - (b.value || 0);
    return 0;
  });

  // TODO: Replace with GET /api/orders/export
  const exportCSV = () => {
    const header = [
      'Tanggal Order',
      'Klien',
      'Judul Project',
      'Tipe',
      'Status',
      'Nilai (IDR)',
      'DP Diterima (IDR)',
      'Sisa (IDR)',
      'Deadline',
    ];
    const rows = sorted.map((c) => {
      const col = data.columns.find((x) => x.id === c.columnId);
      return [
        formatDate(c.createdAt),
        c.client || '',
        c.title,
        PROJECT_TYPES[c.type]?.label || c.type,
        col?.name || '',
        c.value || 0,
        c.dpPaid || 0,
        (c.value || 0) - (c.dpPaid || 0),
        formatDate(c.dueDate),
      ];
    });
    const csv = [header, ...rows]
      .map((r) =>
        r.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(',')
      )
      .join('\n');
    const a = document.createElement('a');
    a.href =
      'data:text/csv;charset=utf-8,\uFEFF' + encodeURIComponent(csv);
    a.download = `promptara-orders-${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
  };

  const getColName = (colId) =>
    (data.columns || []).find((c) => c.id === colId)?.name || '—';
  const getColColor = (colId) =>
    (data.columns || []).find((c) => c.id === colId)?.color || '#9090AA';

  const totalValue = sorted.reduce((s, c) => s + (c.value || 0), 0);
  const totalReceived = sorted.reduce(
    (s, c) => s + (c.dpPaid || 0),
    0
  );
  const totalOutstanding = totalValue - totalReceived;

  const filterSelectClass =
    'border border-line rounded-[9px] py-[7px] px-2.5 text-xs text-ink bg-surface outline-none cursor-pointer';

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* Header */}
      <div
        className="px-6 pt-[18px] pb-3.5 border-b bg-white shrink-0"
        style={{ borderColor: '#E5E4EF' }}
      >
        <div className="flex items-start justify-between mb-3.5 gap-3">
          <div>
            <h2 className="m-0 text-lg font-extrabold text-ink tracking-[-0.4px]">
              Riwayat Order
            </h2>
            <p
              className="m-0 mt-[2px] text-xs"
              style={{ color: '#9090AA' }}
            >
              Semua project yang masuk ke PROMPTARA
            </p>
          </div>
          <div className="flex gap-2">
            <Btn onClick={exportCSV} variant="secondary" small>
              <Icon name="download" size={13} color="#5C5C7A" /> Export
              CSV
            </Btn>
            <Btn onClick={() => setAddOpen(true)} small>
              <Icon
                name="plus"
                size={13}
                color="#fff"
                strokeWidth={2.5}
              />{' '}
              Tambah Order
            </Btn>
          </div>
        </div>

        {/* Stats band */}
        <div
          className="flex mb-3.5 bg-white rounded-xl overflow-hidden"
          style={{ border: '1.5px solid #E5E4EF' }}
        >
          {[
            {
              label: 'Total Nilai',
              value: formatIDR(totalValue),
              color: '#17172E',
            },
            {
              label: 'Diterima',
              value: formatIDR(totalReceived),
              color: '#22C55E',
            },
            {
              label: 'Outstanding',
              value: formatIDR(totalOutstanding),
              color: '#F59E0B',
            },
            {
              label: 'Total Order',
              value: `${sorted.length} project`,
              color: '#3EB8B8',
            },
          ].map((s, i, arr) => (
            <div
              key={s.label}
              className="flex-1 py-3 px-[18px]"
              style={{
                borderRight:
                  i < arr.length - 1 ? '1px solid #ECEAF4' : 'none',
              }}
            >
              <div
                className="text-[10px] font-bold uppercase tracking-[0.8px] mb-1"
                style={{ color: '#B0AFBF' }}
              >
                {s.label}
              </div>
              <div
                className="text-sm font-extrabold tracking-[-0.3px]"
                style={{ color: s.color }}
              >
                {s.value}
              </div>
            </div>
          ))}
        </div>

        {/* Filters */}
        <div className="flex gap-2 flex-wrap">
          <div className="relative">
            <div className="absolute left-2.5 top-1/2 -translate-y-1/2">
              <Icon name="search" size={13} color="#9090AA" />
            </div>
            <input
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Cari klien / project..."
              className="border border-line rounded-[9px] py-[7px] pl-[30px] pr-2.5 text-xs text-ink bg-surface outline-none"
              style={{ width: 200, fontFamily: 'inherit' }}
            />
          </div>
          {[
            {
              val: filterType,
              set: setFilterType,
              opts: [
                ['all', 'Semua Tipe'],
                ...Object.entries(PROJECT_TYPES).map(([k, v]) => [
                  k,
                  v.label,
                ]),
              ],
            },
            {
              val: filterCol,
              set: setFilterCol,
              opts: [
                ['all', 'Semua Status'],
                ...(data.columns || []).map((c) => [c.id, c.name]),
              ],
            },
            {
              val: sortBy,
              set: setSortBy,
              opts: [
                ['date-desc', 'Terbaru'],
                ['date-asc', 'Terlama'],
                ['value-desc', 'Nilai ↓'],
                ['value-asc', 'Nilai ↑'],
              ],
            },
          ].map((f, i) => (
            <select
              key={i}
              value={f.val}
              onChange={(e) => f.set(e.target.value)}
              className={filterSelectClass}
              style={{ fontFamily: 'inherit' }}
            >
              {f.opts.map(([v, l]) => (
                <option key={v} value={v}>
                  {l}
                </option>
              ))}
            </select>
          ))}
        </div>
      </div>

      {/* Table */}
      <div className="flex-1 overflow-y-auto px-6 pb-6">
        <table
          className="w-full"
          style={{
            borderCollapse: 'separate',
            borderSpacing: '0 6px',
            marginTop: 10,
          }}
        >
          <thead>
            <tr>
              {[
                'Tanggal',
                'Klien',
                'Project',
                'Tipe',
                'Status',
                'Nilai',
                'DP',
                'Sisa',
                'Deadline',
                'Tim',
              ].map((h) => (
                <th
                  key={h}
                  className="px-3 py-2 text-[10px] font-bold uppercase tracking-[0.5px] whitespace-nowrap sticky top-0 bg-surface z-[2]"
                  style={{
                    color: '#9090AA',
                    textAlign: ['Nilai', 'DP', 'Sisa'].includes(h)
                      ? 'right'
                      : 'left',
                  }}
                >
                  {h}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {sorted.length === 0 && (
              <tr>
                <td
                  colSpan={10}
                  className="py-10 text-center text-[13px]"
                  style={{ color: '#9090AA' }}
                >
                  Belum ada order yang cocok.
                </td>
              </tr>
            )}
            {sorted.map((c) => {
              const outstanding = (c.value || 0) - (c.dpPaid || 0);
              const paidPct =
                c.value > 0
                  ? Math.min(
                      100,
                      Math.round((c.dpPaid / c.value) * 100)
                    )
                  : 0;
              const colColor = getColColor(c.columnId);
              const overdue = isOverdue(c.dueDate);
              return (
                <tr
                  key={c.id}
                  onClick={() => setEditId(c.id)}
                  className="cursor-pointer"
                  onMouseEnter={(e) =>
                    [...e.currentTarget.cells].forEach(
                      (td) => (td.style.background = '#E8F7F7')
                    )
                  }
                  onMouseLeave={(e) =>
                    [...e.currentTarget.cells].forEach(
                      (td) => (td.style.background = '#fff')
                    )
                  }
                >
                  <td
                    className="px-3 py-[11px] bg-white text-xs font-medium whitespace-nowrap transition-colors"
                    style={{
                      borderRadius: '10px 0 0 10px',
                      color: '#5C5C7A',
                    }}
                  >
                    {formatDate(c.createdAt)}
                  </td>
                  <td
                    className="px-3 py-[11px] bg-white text-xs font-semibold text-ink whitespace-nowrap transition-colors"
                    style={{
                      maxWidth: 120,
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                    }}
                  >
                    {c.client || '—'}
                  </td>
                  <td
                    className="px-3 py-[11px] bg-white text-xs font-bold text-ink transition-colors"
                    style={{ maxWidth: 200 }}
                  >
                    <div className="overflow-hidden text-ellipsis whitespace-nowrap">
                      {c.title}
                    </div>
                  </td>
                  <td className="px-3 py-[11px] bg-white transition-colors">
                    <TypeBadge type={c.type} small />
                  </td>
                  <td className="px-3 py-[11px] bg-white transition-colors">
                    <span
                      className="text-[11px] font-bold py-[3px] px-[9px] rounded-full whitespace-nowrap"
                      style={{
                        color: colColor,
                        background: colColor + '18',
                      }}
                    >
                      {getColName(c.columnId)}
                    </span>
                  </td>
                  <td className="px-3 py-[11px] bg-white text-xs font-bold text-ink text-right whitespace-nowrap transition-colors">
                    {formatIDR(c.value || 0)}
                  </td>
                  <td className="px-3 py-[11px] bg-white text-right transition-colors">
                    <div
                      className="text-xs font-bold whitespace-nowrap"
                      style={{ color: '#22C55E' }}
                    >
                      {formatIDR(c.dpPaid || 0)}
                    </div>
                    <div
                      className="h-[3px] rounded-full mt-[3px] w-[60px] ml-auto"
                      style={{ background: '#F0FDF4' }}
                    >
                      <div
                        className="h-full rounded-full"
                        style={{
                          width: `${paidPct}%`,
                          background: '#22C55E',
                        }}
                      />
                    </div>
                  </td>
                  <td
                    className="px-3 py-[11px] bg-white text-xs font-bold text-right whitespace-nowrap transition-colors"
                    style={{
                      color: outstanding > 0 ? '#F59E0B' : '#22C55E',
                    }}
                  >
                    {formatIDR(outstanding)}
                  </td>
                  <td
                    className="px-3 py-[11px] bg-white text-[11px] font-semibold whitespace-nowrap transition-colors"
                    style={{
                      color: overdue ? '#EF4444' : '#9090AA',
                    }}
                  >
                    {formatDateShort(c.dueDate)}
                  </td>
                  <td
                    className="px-3 py-[11px] bg-white transition-colors"
                    style={{ borderRadius: '0 10px 10px 0' }}
                  >
                    <div className="flex flex-row-reverse justify-end">
                      {(c.assignees || [])
                        .slice(0, 3)
                        .map((uid, i) => (
                          <div
                            key={uid}
                            style={{
                              marginLeft: i === 0 ? 0 : -6,
                            }}
                          >
                            <Avatar
                              userId={uid}
                              size={22}
                              showRing
                            />
                          </div>
                        ))}
                    </div>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      <Modal
        open={!!editId}
        onClose={() => setEditId(null)}
        width={580}
      >
        {editId && (
          <CardModal
            cardId={editId}
            onClose={() => setEditId(null)}
          />
        )}
      </Modal>
      <Modal
        open={addOpen}
        onClose={() => setAddOpen(false)}
        width={580}
      >
        {addOpen && (
          <CardModal
            isNew
            defaultColumnId={data.columns[0]?.id}
            onClose={() => setAddOpen(false)}
          />
        )}
      </Modal>
    </div>
  );
};

export default OrdersView;
