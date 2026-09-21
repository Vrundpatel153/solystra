import React from 'react';
import { useShop } from '../context/ShopContext';
import { CheckCircle2, Info, X } from 'lucide-react';

export const ToastContainer = () => {
  const { toasts, removeToast } = useShop();

  if (!toasts.length) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col gap-3 max-w-md w-full pointer-events-none px-4 font-sans">
      {toasts.map(toast => (
        <div
          key={toast.id}
          className="pointer-events-auto flex items-start gap-3 p-4 bg-[#380A15] border border-[#C5A059]/40 rounded-xl shadow-2xl text-white animate-slide-up transition-all"
        >
          {toast.type === 'info' ? (
            <Info className="w-5 h-5 text-[#EAD7AE] shrink-0 mt-0.5" />
          ) : (
            <div className="w-5 h-5 rounded-full bg-[#7A152E] flex items-center justify-center shrink-0 text-white mt-0.5 border border-[#C5A059]/40">
              <CheckCircle2 className="w-3.5 h-3.5" />
            </div>
          )}
          <div className="flex-1 text-xs font-medium text-[#FAF8F5]">
            {toast.message}
          </div>
          <button
            onClick={() => removeToast(toast.id)}
            className="text-[#FAF8F5]/60 hover:text-white shrink-0"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      ))}
    </div>
  );
};
