
import React from 'react';

const Hero = () => {
  return (
    <section className='bg-gray-200 text-center py-20'>
      <h1 className='text-4xl font-bold mb-4'>Revolutionizing AI Solutions for Your Business</h1>
      <p className='text-xl mb-8'>Innovative, Scalable, and Tailored AI Software Solutions</p>
      <div className='space-x-4'>
        <button className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'>
          Learn More
        </button>
        <button className='bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded'>
          Get a Quote
        </button>
      </div>
    </section>
  );
}

export default Hero;