import React from 'react';

const HeroSection: React.FC = () => {
    return (
        <div className='hero bg-blue-500 text-white p-20 text-center'>
            <h1 className='text-4xl font-bold'>Welcome to the Art Gallery</h1>
            <p className='mt-4'>Discover beautiful drawings from talented artists around the world.</p>
            <button className='mt-8 bg-green-500 text-white py-2 px-4 rounded'>Explore Now</button>
        </div>
    );
};

export default HeroSection;