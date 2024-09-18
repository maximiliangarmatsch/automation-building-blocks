import React from 'react';

function Hero() {
  return (
    <section className='bg-cover bg-center h-screen' style={{ backgroundImage: 'url(https://example.com/hero-bg.jpg)' }}>
      <div className='container mx-auto h-full flex flex-col justify-center items-center text-center text-white'>
        <h1 className='text-5xl font-bold mb-4'>Transforming Ideas into Intelligent Solutions</h1>
        <h2 className='text-2xl mb-8'>Unlock the power of AI with our cutting-edge software solutions</h2>
        <div className='space-x-4'>
          <a href='#learn-more' className='bg-gray-600 text-white px-6 py-3 rounded'>Learn More</a>
          <a href='#get-started' className='bg-blue-600 text-white px-6 py-3 rounded'>Get Started</a>
        </div>
      </div>
    </section>
  );
}

export default Hero;
