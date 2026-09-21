import React, { useState, useEffect } from 'react';
import { useShop } from './context/ShopContext';
import { AnnouncementBar } from './components/AnnouncementBar';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { CartDrawer } from './components/CartDrawer';
import { WishlistDrawer } from './components/WishlistDrawer';
import { SearchModal } from './components/SearchModal';
import { QuickViewModal } from './components/QuickViewModal';
import { ToastContainer } from './components/Toast';
import { MobileBottomBar } from './components/MobileBottomBar';
import { BoutiqueModal } from './components/BoutiqueModal';
import { HomePage } from './pages/HomePage';
import { ProductDetailPage } from './pages/ProductDetailPage';
import { CheckoutPage } from './pages/CheckoutPage';
import { TermsPage } from './pages/TermsPage';
import { PrivacyPolicyPage } from './pages/PrivacyPolicyPage';
import { OffersPage } from './pages/OffersPage';
import { AllProductsPage } from './pages/AllProductsPage';

export const App = () => {
  const parseRoute = () => {
    const hash = window.location.hash || '';
    const path = window.location.pathname || '';

    // Check checkout route: #/checkout or /checkout
    if (hash === '#/checkout' || hash.startsWith('#/checkout') || path === '/checkout') {
      return { isCheckout: true, isTerms: false, isPrivacy: false, isProduct: false, isOffers: false, isProducts: false, id: null };
    }

    // Check offers route: #/offers, /offers
    if (hash === '#/offers' || hash.startsWith('#/offers') || path === '/offers') {
      return { isOffers: true, isProducts: false, isCheckout: false, isTerms: false, isPrivacy: false, isProduct: false, id: null };
    }

    // Check all products / explore catalog route: #/products, #/catalog, #/explore, /products, /catalog
    if (
      hash === '#/products' ||
      hash.startsWith('#/products') ||
      hash === '#/catalog' ||
      hash.startsWith('#/catalog') ||
      hash === '#/explore' ||
      hash.startsWith('#/explore') ||
      path === '/products' ||
      path === '/catalog'
    ) {
      return { isProducts: true, isOffers: false, isCheckout: false, isTerms: false, isPrivacy: false, isProduct: false, id: null };
    }

    // Check privacy policy route: #/privacy, #/privacy-policy, /privacy, /privacy-policy
    if (
      hash === '#/privacy' ||
      hash.startsWith('#/privacy') ||
      hash === '#/privacy-policy' ||
      hash.startsWith('#/privacy-policy') ||
      path === '/privacy' ||
      path === '/privacy-policy' ||
      path === '/policies/privacy-policy'
    ) {
      return { isPrivacy: true, isTerms: false, isCheckout: false, isProduct: false, isOffers: false, isProducts: false, id: null };
    }

    // Check terms and conditions route: #/terms, #/terms-and-conditions, /terms
    if (
      hash === '#/terms' ||
      hash.startsWith('#/terms') ||
      hash === '#/terms-and-conditions' ||
      hash.startsWith('#/terms-and-conditions') ||
      path === '/terms' ||
      path === '/terms-and-conditions' ||
      path === '/policies/terms-of-service'
    ) {
      return { isTerms: true, isPrivacy: false, isCheckout: false, isProduct: false, isOffers: false, isProducts: false, id: null };
    }

    // Check hash route first: #/product/:id
    if (hash.startsWith('#/product/')) {
      const id = hash.replace('#/product/', '').split('?')[0];
      return { isProduct: true, isCheckout: false, isTerms: false, isPrivacy: false, isOffers: false, isProducts: false, id };
    }

    // Check pathname route: /product/:id (for Netlify full routing)
    if (path.startsWith('/product/')) {
      const id = path.replace('/product/', '').split('/')[0].split('?')[0];
      return { isProduct: true, isCheckout: false, isTerms: false, isPrivacy: false, isOffers: false, isProducts: false, id };
    }

    return { isProduct: false, isCheckout: false, isTerms: false, isPrivacy: false, isOffers: false, isProducts: false, id: null };
  };

  const [currentRoute, setCurrentRoute] = useState(parseRoute);
  const [activeCategory, setActiveCategory] = useState('all');
  const [isBoutiqueOpen, setIsBoutiqueOpen] = useState(false);

  useEffect(() => {
    const handleRouteChange = () => {
      setCurrentRoute(parseRoute());
      window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    window.addEventListener('hashchange', handleRouteChange);
    window.addEventListener('popstate', handleRouteChange);

    return () => {
      window.removeEventListener('hashchange', handleRouteChange);
      window.removeEventListener('popstate', handleRouteChange);
    };
  }, []);

  const navigateToHome = (category = 'all') => {
    setActiveCategory(category);
    if (
      currentRoute.isProduct ||
      currentRoute.isCheckout ||
      currentRoute.isTerms ||
      currentRoute.isPrivacy ||
      currentRoute.isOffers ||
      currentRoute.isProducts
    ) {
      window.location.hash = '#/';
      // Also update history if using pathname
      if (window.location.pathname !== '/' && window.location.pathname !== '/index.html') {
        window.history.pushState(null, '', '/');
      }
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-[#FAF8F5] selection:bg-[#7A152E] selection:text-white font-sans pb-16 lg:pb-0">
      {/* If on checkout page, show distraction-free luxury checkout */}
      {currentRoute.isCheckout ? (
        <CheckoutPage onBackToStore={() => navigateToHome('all')} />
      ) : (
        <>
          {/* Announcement Bar */}
          <AnnouncementBar />

          {/* Luxury Sticky Navbar (Bluorng-Inspired Architecture) */}
          <Navbar
            activeCategory={activeCategory}
            onSelectCategory={navigateToHome}
            onOpenBoutique={() => setIsBoutiqueOpen(true)}
          />

          {/* Main Viewport Content */}
          <main className="flex-1">
            {currentRoute.isPrivacy ? (
              <PrivacyPolicyPage onBackToStore={() => navigateToHome('all')} />
            ) : currentRoute.isTerms ? (
              <TermsPage onBackToStore={() => navigateToHome('all')} />
            ) : currentRoute.isOffers ? (
              <OffersPage onBackToStore={() => navigateToHome('all')} />
            ) : currentRoute.isProducts ? (
              <AllProductsPage onBackToStore={() => navigateToHome('all')} />
            ) : currentRoute.isProduct && currentRoute.id ? (
              <ProductDetailPage productId={currentRoute.id} />
            ) : (
              <HomePage
                activeCategory={activeCategory}
                onSelectCategory={setActiveCategory}
              />
            )}
          </main>

          {/* Multi-Column Luxury Footer */}
          <Footer />

          {/* Mobile Floating Bottom Bar (Hidden on Product Detail Page to allow sticky Buy Now / Add to Cart CTA popup) */}
          {!currentRoute.isProduct && (
            <MobileBottomBar
              onOpenBoutique={() => setIsBoutiqueOpen(true)}
            />
          )}
        </>
      )}

      {/* Boutique & Flagship Ateliers Modal */}
      <BoutiqueModal
        isOpen={isBoutiqueOpen}
        onClose={() => setIsBoutiqueOpen(false)}
      />

      {/* Global Modals & Drawers */}
      <CartDrawer />
      <WishlistDrawer />
      <SearchModal />
      <QuickViewModal />
      <ToastContainer />
    </div>
  );
};
