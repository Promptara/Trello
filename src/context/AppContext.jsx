// PROMPTARA — App Context & Reducer
import { createContext, useReducer } from 'react';
import { PromptaraStorage } from '../utils/storage';
import { INITIAL_DATA } from '../constants';

export const AppContext = createContext(null);

export function appReducer(state, action) {
  let next;
  switch (action.type) {
    case 'LOGIN':
      next = { ...state, loggedInUserId: action.userId };
      break;
    case 'LOGOUT':
      next = { ...state, loggedInUserId: null };
      break;
    case 'ADD_USER':
      next = { ...state, users: [...state.users, action.user] };
      break;
    case 'SET_BOARD':
      next = { ...state, activeBoardId: action.boardId };
      break;
    case 'ADD_BOARD':
      next = {
        ...state,
        boards: [...(state.boards || []), action.board],
        activeBoardId: action.board.id,
      };
      break;
    case 'DELETE_BOARD':
      next = {
        ...state,
        boards: (state.boards || []).filter((b) => b.id !== action.boardId),
        cards: state.cards.filter((c) => c.boardId !== action.boardId),
        activeBoardId:
          state.activeBoardId === action.boardId
            ? state.boards[0]?.id || null
            : state.activeBoardId,
      };
      break;
    case 'ADD_CARD':
      next = { ...state, cards: [action.card, ...state.cards] };
      break;
    case 'UPDATE_CARD':
      next = {
        ...state,
        cards: state.cards.map((c) =>
          c.id === action.cardId ? { ...c, ...action.updates } : c
        ),
      };
      break;
    case 'DELETE_CARD':
      next = {
        ...state,
        cards: state.cards.filter((c) => c.id !== action.cardId),
      };
      break;
    case 'ADD_COMMENT':
      next = {
        ...state,
        cards: state.cards.map((c) =>
          c.id === action.cardId
            ? { ...c, comments: [...(c.comments || []), action.comment] }
            : c
        ),
      };
      break;
    case 'MARK_NOTIF_READ':
      next = {
        ...state,
        notifications: state.notifications.map((n) =>
          n.id === action.id ? { ...n, read: true } : n
        ),
      };
      break;
    case 'MARK_ALL_READ':
      next = {
        ...state,
        notifications: state.notifications.map((n) => ({ ...n, read: true })),
      };
      break;
    default:
      return state;
  }
  PromptaraStorage.save(next);
  return next;
}

export function useAppState() {
  const saved = PromptaraStorage.load();
  return useReducer(appReducer, saved || INITIAL_DATA);
}
