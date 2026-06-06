// PROMPTARA — Root App Component
import { useState } from 'react';
import { AppContext, useAppState } from './context/AppContext';
import Sidebar from './components/Sidebar';
import AuthScreen from './pages/AuthScreen';
import BoardView from './pages/BoardView';
import CalendarView from './pages/CalendarView';
import OrdersView from './pages/OrdersView';
import FinanceView from './pages/FinanceView';
import TeamView from './pages/TeamView';
import './App.css';

const VIEWS = {
  board: BoardView,
  calendar: CalendarView,
  orders: OrdersView,
  finance: FinanceView,
  team: TeamView,
};

const App = () => {
  const [data, dispatch] = useAppState();
  const [view, setView] = useState('board');

  const currentUser = data.users.find(
    (u) => u.id === data.loggedInUserId
  );
  const unread = (data.notifications || []).filter(
    (n) => !n.read
  ).length;

  if (!currentUser) {
    return (
      <AppContext.Provider value={{ data, dispatch }}>
        <AuthScreen onLogin={() => {}} />
      </AppContext.Provider>
    );
  }

  const ActiveView = VIEWS[view] || BoardView;

  return (
    <AppContext.Provider value={{ data, dispatch }}>
      <div
        className="flex h-screen overflow-hidden bg-surface"
        style={{ fontFamily: "'Plus Jakarta Sans', sans-serif" }}
      >
        <Sidebar
          view={view}
          setView={setView}
          currentUser={currentUser}
          unread={unread}
        />
        <main className="flex-1 overflow-hidden flex flex-col">
          <ActiveView />
        </main>
      </div>
    </AppContext.Provider>
  );
};

export default App;
