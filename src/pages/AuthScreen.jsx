// PROMPTARA — Auth Screen (Login / Register)
import { useState, useContext } from 'react';
import { AppContext } from '../context/AppContext';
import { genId } from '../utils/storage';
import Icon from '../components/ui/Icon';
import SpaceField from '../components/SpaceField';

const AuthScreen = ({ onLogin }) => {
  const [tab, setTab] = useState('login');
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPass, setLoginPass] = useState('');
  const [loginErr, setLoginErr] = useState('');
  const [regName, setRegName] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regPass, setRegPass] = useState('');
  const [regRole, setRegRole] = useState('Designer');
  const [regErr, setRegErr] = useState('');

  const { data, dispatch } = useContext(AppContext);

  // TODO: Replace with POST /api/auth/login
  const handleLogin = (e) => {
    e.preventDefault();
    const u = data.users.find(
      (u) => u.email === loginEmail && u.password === loginPass
    );
    if (!u) {
      setLoginErr('Email atau password salah.');
      return;
    }
    dispatch({ type: 'LOGIN', userId: u.id });
    onLogin(u);
  };

  // TODO: Replace with POST /api/auth/register
  const handleRegister = (e) => {
    e.preventDefault();
    if (!regName || !regEmail || !regPass) {
      setRegErr('Semua field wajib diisi.');
      return;
    }
    if (data.users.find((u) => u.email === regEmail)) {
      setRegErr('Email sudah terdaftar.');
      return;
    }
    const initials = regName
      .trim()
      .split(' ')
      .map((w) => w[0].toUpperCase())
      .slice(0, 2)
      .join('');
    const colors = [
      '#3EB8B8',
      '#EC4899',
      '#22C55E',
      '#F97316',
      '#8B5CF6',
      '#14B8A6',
    ];
    const color = colors[data.users.length % colors.length];
    const newUser = {
      id: genId(),
      name: regName,
      email: regEmail,
      password: regPass,
      role: regRole,
      initials,
      color,
    };
    dispatch({ type: 'ADD_USER', user: newUser });
    dispatch({ type: 'LOGIN', userId: newUser.id });
    onLogin(newUser);
  };

  const fieldStyle = {
    width: '100%',
    border: 'none',
    borderBottom: '1.5px solid #E5E4EF',
    background: 'transparent',
    padding: '10px 0',
    fontSize: 14,
    fontFamily: 'inherit',
    color: '#17172E',
    outline: 'none',
    transition: 'border-color .15s',
  };

  const FEATURES = [
    'Kanban board dengan 5 stage custom',
    'Riwayat order & tracking klien',
    'Rekap keuangan otomatis',
  ];

  return (
    <div
      className="min-h-screen flex"
      style={{ fontFamily: "'Plus Jakarta Sans', sans-serif" }}
    >
      {/* ── Left dark panel ─────────────────── */}
      <div
        className="w-[440px] shrink-0 flex flex-col p-[52px_48px] relative overflow-hidden"
        style={{ background: '#0F0F1C' }}
      >
        <SpaceField />
        <div
          className="absolute top-0 right-0 w-[2px] h-[35%] opacity-70"
          style={{ background: '#3EB8B8' }}
        />

        <div className="relative z-[1] flex flex-col h-full">
          <div className="mb-auto">
            <img
              src="/logo.png"
              alt="PROMPTARA.AI"
              className="h-[52px] block"
              style={{ opacity: 0.95 }}
            />
          </div>

          <div className="pt-14">
            <h1 className="text-[44px] font-extrabold text-white leading-[1.08] tracking-[-1.8px] mb-[22px]">
              Creative
              <br />
              <span style={{ color: '#3EB8B8' }}>Agency</span>
              <br />
              Workspace.
            </h1>
            <p
              className="text-sm leading-[1.75] max-w-[280px] mb-10"
              style={{ color: 'rgba(255,255,255,0.45)' }}
            >
              Kelola project, tim, dan keuangan agency kamu — semua dalam
              satu tempat yang rapi.
            </p>

            <div className="flex flex-col gap-[11px]">
              {FEATURES.map((f) => (
                <div key={f} className="flex items-center gap-2.5">
                  <div
                    className="w-4 h-4 rounded shrink-0 flex items-center justify-center"
                    style={{
                      border: '1px solid rgba(62,184,184,0.5)',
                      background: 'rgba(62,184,184,0.12)',
                    }}
                  >
                    <Icon
                      name="check"
                      size={9}
                      color="#3EB8B8"
                      strokeWidth={2.8}
                    />
                  </div>
                  <span
                    className="text-[13px] font-medium"
                    style={{ color: 'rgba(255,255,255,0.55)' }}
                  >
                    {f}
                  </span>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-auto pt-12">
            <span
              className="text-[10px] tracking-[1px] uppercase"
              style={{ color: 'rgba(255,255,255,0.2)' }}
            >
              v1.0 · 2026
            </span>
          </div>
        </div>
      </div>

      {/* ── Right form panel ────────────────── */}
      <div
        className="flex-1 flex items-center justify-center p-[48px_40px]"
        style={{ background: '#FAFAF8' }}
      >
        <div className="w-full max-w-[360px]">
          <div className="mb-9">
            <h2 className="text-[22px] font-extrabold text-ink tracking-[-0.5px] mb-[5px]">
              {tab === 'login'
                ? 'Selamat datang kembali'
                : 'Buat akun baru'}
            </h2>
            <p
              className="text-[13px] font-medium"
              style={{ color: '#9090AA' }}
            >
              {tab === 'login'
                ? 'Masuk ke workspace PROMPTARA kamu.'
                : 'Bergabung dengan tim PROMPTARA.'}
            </p>
          </div>

          {/* Tabs */}
          <div className="flex gap-6 mb-8 border-b border-line">
            {['login', 'register'].map((t) => (
              <button
                key={t}
                onClick={() => {
                  setTab(t);
                  setLoginErr('');
                  setRegErr('');
                }}
                className="pb-3 border-none bg-transparent cursor-pointer font-bold text-sm transition-all"
                style={{
                  fontFamily: 'inherit',
                  color: tab === t ? '#17172E' : '#B0AFBF',
                  borderBottom:
                    tab === t
                      ? '2px solid #17172E'
                      : '2px solid transparent',
                  marginBottom: -1.5,
                }}
              >
                {t === 'login' ? 'Masuk' : 'Daftar'}
              </button>
            ))}
          </div>

          {tab === 'login' ? (
            <form
              onSubmit={handleLogin}
              className="flex flex-col gap-5"
            >
              <div>
                <label
                  className="block text-[11px] font-bold uppercase tracking-[0.4px] mb-2"
                  style={{ color: '#9090AA' }}
                >
                  Email
                </label>
                <input
                  type="email"
                  value={loginEmail}
                  onChange={(e) => {
                    setLoginEmail(e.target.value);
                    setLoginErr('');
                  }}
                  placeholder="kamu@promptara.id"
                  style={fieldStyle}
                  onFocus={(e) =>
                    (e.target.style.borderBottomColor = '#3EB8B8')
                  }
                  onBlur={(e) =>
                    (e.target.style.borderBottomColor = '#E5E4EF')
                  }
                />
              </div>
              <div>
                <label
                  className="block text-[11px] font-bold uppercase tracking-[0.4px] mb-2"
                  style={{ color: '#9090AA' }}
                >
                  Password
                </label>
                <input
                  type="password"
                  value={loginPass}
                  onChange={(e) => {
                    setLoginPass(e.target.value);
                    setLoginErr('');
                  }}
                  placeholder="••••••••"
                  style={fieldStyle}
                  onFocus={(e) =>
                    (e.target.style.borderBottomColor = '#3EB8B8')
                  }
                  onBlur={(e) =>
                    (e.target.style.borderBottomColor = '#E5E4EF')
                  }
                />
              </div>
              {loginErr && (
                <p className="text-xs font-semibold text-red-500 -mt-2">
                  {loginErr}
                </p>
              )}
              <button
                type="submit"
                className="mt-2 w-full py-[13px] text-white border-none rounded-[10px] cursor-pointer text-sm font-bold tracking-[-0.2px] transition-colors"
                style={{
                  background: '#17172E',
                  fontFamily: 'inherit',
                }}
                onMouseEnter={(e) =>
                  (e.currentTarget.style.background = '#3EB8B8')
                }
                onMouseLeave={(e) =>
                  (e.currentTarget.style.background = '#17172E')
                }
              >
                Masuk ke Workspace
              </button>
            </form>
          ) : (
            <form
              onSubmit={handleRegister}
              className="flex flex-col gap-[18px]"
            >
              {[
                {
                  label: 'Nama Lengkap',
                  val: regName,
                  set: (v) => {
                    setRegName(v);
                    setRegErr('');
                  },
                  ph: 'Nama kamu',
                  type: 'text',
                },
                {
                  label: 'Email',
                  val: regEmail,
                  set: (v) => {
                    setRegEmail(v);
                    setRegErr('');
                  },
                  ph: 'kamu@promptara.id',
                  type: 'email',
                },
                {
                  label: 'Password',
                  val: regPass,
                  set: (v) => {
                    setRegPass(v);
                    setRegErr('');
                  },
                  ph: 'Min. 6 karakter',
                  type: 'password',
                },
              ].map((f) => (
                <div key={f.label}>
                  <label
                    className="block text-[11px] font-bold uppercase tracking-[0.4px] mb-2"
                    style={{ color: '#9090AA' }}
                  >
                    {f.label}
                  </label>
                  <input
                    type={f.type}
                    value={f.val}
                    onChange={(e) => f.set(e.target.value)}
                    placeholder={f.ph}
                    style={fieldStyle}
                    onFocus={(e) =>
                      (e.target.style.borderBottomColor = '#3EB8B8')
                    }
                    onBlur={(e) =>
                      (e.target.style.borderBottomColor = '#E5E4EF')
                    }
                  />
                </div>
              ))}
              <div>
                <label
                  className="block text-[11px] font-bold uppercase tracking-[0.4px] mb-2"
                  style={{ color: '#9090AA' }}
                >
                  Role
                </label>
                <select
                  value={regRole}
                  onChange={(e) => setRegRole(e.target.value)}
                  style={{ ...fieldStyle, cursor: 'pointer' }}
                >
                  {[
                    'Owner',
                    'Designer',
                    'Developer',
                    'Project Manager',
                    'Lainnya',
                  ].map((r) => (
                    <option key={r} value={r}>
                      {r}
                    </option>
                  ))}
                </select>
              </div>
              {regErr && (
                <p className="text-xs font-semibold text-red-500 -mt-1">
                  {regErr}
                </p>
              )}
              <button
                type="submit"
                className="mt-1 w-full py-[13px] text-white border-none rounded-[10px] cursor-pointer text-sm font-bold transition-colors"
                style={{
                  background: '#17172E',
                  fontFamily: 'inherit',
                }}
                onMouseEnter={(e) =>
                  (e.currentTarget.style.background = '#3EB8B8')
                }
                onMouseLeave={(e) =>
                  (e.currentTarget.style.background = '#17172E')
                }
              >
                Buat Akun
              </button>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};

export default AuthScreen;
