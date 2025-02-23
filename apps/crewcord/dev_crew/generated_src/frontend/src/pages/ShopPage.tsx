import React from 'react';
import Navbar from '../components/Navbar';
import ShopGrid from '../components/ShopGrid';
import Footer from '../components/Footer';

const ShopPage: React.FC = () => {
    return (
        <div className='bg-light-grey text-dark-grey'>
            <Navbar />
            <div className='container mx-auto p-10'>
                <h1 className='text-4xl font-bold mb-6'>Shop</h1>
                <ShopGrid />
            </div>
            <Footer />
        </div>
    );
};

export default ShopPage;