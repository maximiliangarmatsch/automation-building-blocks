import React from 'react';
import Navbar from '../components/Navbar';
import HeroSection from '../components/HeroSection';
import CategoriesSection from '../components/CategoriesSection';
import LatestDrawingsSection from '../components/LatestDrawingsSection';
import Footer from '../components/Footer';

const HomePage: React.FC = () => {
    return (
        <div className='bg-light-grey text-dark-grey'>
            <Navbar />
            <HeroSection />
            <CategoriesSection />
            <LatestDrawingsSection />
            <Footer />
        </div>
    );
};

export default HomePage;