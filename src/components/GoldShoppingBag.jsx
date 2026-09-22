import React from 'react';

/**
 * Bespoke Haute Joaillerie Gold Shopping Bag Icon
 * Features:
 * - 24K Champagne Gold multi-stop gradient stroke (#FFF6DB -> #E8CA82 -> #D4AF37 -> #967226)
 * - Soft translucent metallic inner radiance fill
 * - Signature atelier boutique fold & arched satin ribbon handle
 * - Delicate solitaire jewel starburst glint
 */
export const GoldShoppingBag = ({ className = "w-4 h-4 shrink-0" }) => (
  <svg
    className={className}
    viewBox="0 0 24 24"
    fill="none"
    xmlns="http://www.w3.org/2000/svg"
    aria-hidden="true"
  >
    <defs>
      {/* 24K Luminous Champagne Gold Gradient */}
      <linearGradient id="solystraChampagneGold" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" stopColor="#FFF6D8" />
        <stop offset="35%" stopColor="#F9E2A8" />
        <stop offset="70%" stopColor="#E5BE64" />
        <stop offset="100%" stopColor="#D4AF37" />
      </linearGradient>
    </defs>

    {/* Luxury Boutique Bag Body */}
    <path
      d="M6 2L3 6V20C3 21.1 3.9 22 5 22H19C20.1 22 21 21.1 21 20V6L18 2H6Z"
      stroke="url(#solystraChampagneGold)"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />

    {/* Crisp Atelier Bag Mouth Rim */}
    <path
      d="M3 6H21"
      stroke="url(#solystraChampagneGold)"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />

    {/* Elegant Ribbon Handle */}
    <path
      d="M16 10C16 12.21 14.21 14 12 14C9.79 14 8 12.21 8 10"
      stroke="url(#solystraChampagneGold)"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);
