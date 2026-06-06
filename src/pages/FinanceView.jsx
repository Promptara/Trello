// PROMPTARA — Finance Dashboard
import { useContext } from 'react';
import { AppContext } from '../context/AppContext';
import { PROJECT_TYPES } from '../constants';
import { formatIDR, formatDate } from '../utils/formatters';
import Icon from '../components/common/ui/Icon';
import Btn from '../components/common/ui/Btn';

const FinanceView = () => {
  const { data } = useContext(AppContext);
  const cards = data.cards || [];
  // TODO: Replace with GET /api/finance/summary
  const orders = cards.filter((c) => c.value > 0);

  /* ── Aggregates ── */
  const totalValue = orders.reduce((s, c) => s + (c.value || 0), 0);
  const totalReceived = orders.reduce(
    (s, c) => s + (c.dpPaid || 0),
    0
  );
  const totalOutstanding = totalValue - totalReceived;
  const doneRevenue = orders
    .filter((c) => c.columnId === 'col5')
    .reduce((s, c) => s + (c.value || 0), 0);

  /* ── Monthly data (last 6 months) ── */
  const months = [];
  for (let i = 5; i >= 0; i--) {
    const d = new Date();
    d.setMonth(d.getMonth() - i);
    months.push({
      key: `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`,
      label: d.toLocaleDateString('id-ID', {
        month: 'short',
        year: '2-digit',
      }),
    });
  }

  const monthlyData = months.map((m) => {
    const mo = orders.filter((c) => c.createdAt?.slice(0, 7) === m.key);
    return {
      ...m,
      value: mo.reduce((s, c) => s + (c.value || 0), 0),
      received: mo.reduce((s, c) => s + (c.dpPaid || 0), 0),
      count: mo.length,
    };
  });

  const maxVal = Math.max(...monthlyData.map((m) => m.value), 1);

  /* ── By type ── */
  const byType = Object.entries(PROJECT_TYPES)
    .map(([key, cfg]) => {
      const typeOrders = orders.filter((c) => c.type === key);
      return {
        key,
        ...cfg,
        value: typeOrders.reduce((s, c) => s + (c.value || 0), 0),
        count: typeOrders.length,
      };
    })
    .filter((t) => t.count > 0)
    .sort((a, b) => b.value - a.value);

  /* ── By status ── */
  const byStatus = (data.columns || [])
    .map((col) => {
      const colOrders = orders.filter((c) => c.columnId === col.id);
      return {
        ...col,
        value: colOrders.reduce((s, c) => s + (c.value || 0), 0),
        count: colOrders.length,
      };
    })
    .filter((c) => c.count > 0);

  /* ── Recent orders ── */
  const recent = [...orders]
    .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
    .slice(0, 6);

  // TODO: Replace with GET /api/finance/export
  const exportCSV = () => {
    const header = [
      'Bulan',
      'Total Nilai (IDR)',
      'Total Diterima (IDR)',
      'Jumlah Order',
    ];
    const rows = monthlyData.map((m) => [
      m.label,
      m.value,
      m.received,
      m.count,
    ]);
    const csv = [header, ...rows]
      .map((r) =>
        r.map((v) => `"${String(v).replace(/"/g, '""')}"`).join(',')
      )
      .join('\n');
    const a = document.createElement('a');
    a.href =
      'data:text/csv;charset=utf-8,\uFEFF' + encodeURIComponent(csv);
    a.download = `promptara-finance-${new Date().toISOString().slice(0, 7)}.csv`;
    a.click();
  };

  const cardClass = 'bg-white rounded-[14px] p-5';
  const cardStyle = { border: '1.5px solid #E5E4EF' };

  return (
    <div className="h-full overflow-y-auto p-6 flex flex-col gap-5">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="m-0 text-lg font-extrabold text-ink tracking-[-0.4px]">
            Rekap Keuangan
          </h2>
          <p
            className="m-0 mt-[2px] text-xs"
            style={{ color: '#9090AA' }}
          >
            Terhubung otomatis dari data order · {orders.length} project
            aktif
          </p>
        </div>
        <Btn onClick={exportCSV} variant="secondary" small>
          <Icon name="download" size={13} color="#5C5C7A" /> Export CSV
        </Btn>
      </div>

      {/* Stat band */}
      <div
        className="bg-white rounded-[14px] p-[22px_28px] flex gap-0"
        style={cardStyle}
      >
        {[
          {
            label: 'Total Nilai Project',
            value: formatIDR(totalValue),
            sub: `${orders.length} project berbayar`,
            accent: '#17172E',
          },
          {
            label: 'Total Diterima',
            value: formatIDR(totalReceived),
            sub: `${totalValue > 0 ? Math.round((totalReceived / totalValue) * 100) : 0}% dari total`,
            accent: '#22C55E',
          },
          {
            label: 'Outstanding',
            value: formatIDR(totalOutstanding),
            sub: 'Belum diterima',
            accent: '#F59E0B',
          },
          {
            label: 'Done Deal Revenue',
            value: formatIDR(doneRevenue),
            sub: 'Project selesai',
            accent: '#3EB8B8',
          },
        ].map((s, i, arr) => (
          <div
            key={s.label}
            style={{
              flex: 1,
              paddingLeft: i === 0 ? 0 : 28,
              paddingRight: i === arr.length - 1 ? 0 : 28,
              borderLeft: i > 0 ? '1px solid #ECEAF4' : 'none',
            }}
          >
            <div
              className="text-[10px] font-bold uppercase tracking-[1px] mb-1.5"
              style={{ color: '#B0AFBF' }}
            >
              {s.label}
            </div>
            <div
              className="text-[20px] font-extrabold tracking-[-0.5px] mb-[3px] leading-none"
              style={{ color: s.accent }}
            >
              {s.value}
            </div>
            <div
              className="text-[11px] font-medium"
              style={{ color: '#B0AFBF' }}
            >
              {s.sub}
            </div>
          </div>
        ))}
      </div>

      {/* Overall payment progress */}
      {totalValue > 0 && (
        <div
          className="bg-white rounded-xl p-[14px_20px]"
          style={cardStyle}
        >
          <div className="flex justify-between mb-2">
            <span
              className="text-[11px] font-bold tracking-[0.3px]"
              style={{ color: '#9090AA' }}
            >
              Progress Pembayaran Keseluruhan
            </span>
            <span className="text-xs font-extrabold text-ink">
              {Math.round((totalReceived / totalValue) * 100)}%
            </span>
          </div>
          <div
            className="h-1.5 rounded-full"
            style={{ background: '#F0EFF8' }}
          >
            <div
              className="h-full rounded-full transition-all"
              style={{
                width: `${Math.round((totalReceived / totalValue) * 100)}%`,
                background: 'linear-gradient(90deg, #3EB8B8, #22C55E)',
              }}
            />
          </div>
        </div>
      )}

      {/* Monthly Chart + By Type */}
      <div
        className="grid gap-4"
        style={{ gridTemplateColumns: '1.6fr 1fr' }}
      >
        {/* Monthly bar chart */}
        <div className={cardClass} style={cardStyle}>
          <div className="flex justify-between items-center mb-[18px]">
            <h3 className="m-0 text-sm font-bold text-ink">
              Nilai Project per Bulan
            </h3>
            <div className="flex gap-3 items-center">
              {[
                ['#3EB8B8', 'Nilai'],
                ['#22C55E', 'Diterima'],
              ].map(([color, label]) => (
                <div key={label} className="flex items-center gap-1">
                  <div
                    className="w-2.5 h-2.5 rounded-[3px]"
                    style={{ background: color }}
                  />
                  <span
                    className="text-[10px] font-semibold"
                    style={{ color: '#9090AA' }}
                  >
                    {label}
                  </span>
                </div>
              ))}
            </div>
          </div>
          <div
            className="flex gap-2.5 items-end"
            style={{ height: 150 }}
          >
            {monthlyData.map((m) => {
              const valH =
                maxVal > 0 ? (m.value / maxVal) * 130 : 0;
              const recH =
                maxVal > 0 ? (m.received / maxVal) * 130 : 0;
              return (
                <div
                  key={m.key}
                  className="flex-1 flex flex-col items-center gap-1"
                  title={`${m.label}: ${formatIDR(m.value)}`}
                >
                  <div
                    className="text-[9px] font-semibold mb-[2px]"
                    style={{ color: '#9090AA' }}
                  >
                    {m.count > 0 ? m.count : ''}
                  </div>
                  <div
                    className="w-full flex gap-[2px] items-end"
                    style={{ height: 130 }}
                  >
                    <div
                      className="flex-1 rounded-t transition-all"
                      style={{
                        height: Math.max(
                          valH,
                          m.value > 0 ? 4 : 0
                        ),
                        background: '#3EB8B8',
                        minHeight: m.value > 0 ? 4 : 0,
                      }}
                    />
                    <div
                      className="flex-1 rounded-t transition-all"
                      style={{
                        height: Math.max(
                          recH,
                          m.received > 0 ? 4 : 0
                        ),
                        background: '#22C55E',
                        minHeight: m.received > 0 ? 4 : 0,
                      }}
                    />
                  </div>
                  <span
                    className="text-[9px] font-semibold mt-[2px]"
                    style={{ color: '#9090AA' }}
                  >
                    {m.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* By type breakdown */}
        <div className={cardClass} style={cardStyle}>
          <h3 className="m-0 mb-4 text-sm font-bold text-ink">
            Per Tipe Project
          </h3>
          <div className="flex flex-col gap-[11px]">
            {byType.length === 0 && (
              <p
                className="text-xs m-0"
                style={{ color: '#9090AA' }}
              >
                Belum ada data.
              </p>
            )}
            {byType.map((t) => {
              const pct =
                totalValue > 0
                  ? (t.value / totalValue) * 100
                  : 0;
              return (
                <div key={t.key}>
                  <div className="flex justify-between mb-[5px]">
                    <div className="flex items-center gap-[7px]">
                      <div
                        className="w-2 h-2 rounded-full"
                        style={{ background: t.color }}
                      />
                      <span className="text-xs font-semibold text-ink">
                        {t.label}
                      </span>
                      <span
                        className="text-[10px] font-medium"
                        style={{ color: '#9090AA' }}
                      >
                        ({t.count})
                      </span>
                    </div>
                    <span className="text-xs font-bold text-ink">
                      {formatIDR(t.value)}
                    </span>
                  </div>
                  <div
                    className="h-[5px] rounded-full"
                    style={{ background: '#F0EFF8' }}
                  >
                    <div
                      className="h-full rounded-full transition-all"
                      style={{
                        width: `${pct}%`,
                        background: t.color,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* By Status + Recent */}
      <div
        className="grid gap-4"
        style={{ gridTemplateColumns: '1fr 1.6fr' }}
      >
        {/* By status */}
        <div className={cardClass} style={cardStyle}>
          <h3 className="m-0 mb-3.5 text-sm font-bold text-ink">
            Per Status Pengerjaan
          </h3>
          <div className="flex flex-col gap-2">
            {byStatus.map((s) => (
              <div
                key={s.id}
                className="flex items-center gap-2.5 bg-surface rounded-[10px] py-[10px] px-3"
              >
                <div
                  className="w-[9px] h-[9px] rounded-full shrink-0"
                  style={{ background: s.color }}
                />
                <span className="flex-1 text-xs font-semibold text-ink">
                  {s.name}
                </span>
                <span
                  className="text-[11px] font-bold"
                  style={{ color: s.color }}
                >
                  {s.count} project
                </span>
                <span
                  className="text-[11px] font-bold"
                  style={{ color: '#5C5C7A' }}
                >
                  {formatIDR(s.value)}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Recent orders */}
        <div className={cardClass} style={cardStyle}>
          <h3 className="m-0 mb-3.5 text-sm font-bold text-ink">
            Order Terbaru
          </h3>
          <div className="flex flex-col gap-2">
            {recent.map((c) => {
              const colColor =
                (data.columns || []).find(
                  (x) => x.id === c.columnId
                )?.color || '#9090AA';
              const paidPct =
                c.value > 0
                  ? Math.min(
                      100,
                      Math.round((c.dpPaid / c.value) * 100)
                    )
                  : 0;
              return (
                <div
                  key={c.id}
                  className="flex items-center gap-2.5 py-[9px] px-3 bg-surface rounded-[10px]"
                  style={{ borderLeft: `3px solid ${colColor}` }}
                >
                  <div className="flex-1 min-w-0">
                    <div className="text-xs font-bold text-ink overflow-hidden text-ellipsis whitespace-nowrap">
                      {c.title}
                    </div>
                    <div
                      className="text-[10px] mt-[1px]"
                      style={{ color: '#9090AA' }}
                    >
                      {c.client} · {formatDate(c.createdAt)}
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-xs font-extrabold text-ink">
                      {formatIDR(c.value)}
                    </div>
                    <div
                      className="text-[10px] font-semibold"
                      style={{ color: '#22C55E' }}
                    >
                      {paidPct}% diterima
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
};

export default FinanceView;
