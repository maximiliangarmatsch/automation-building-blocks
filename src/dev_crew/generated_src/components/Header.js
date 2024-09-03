
import React from 'react';

const Header = () => {
  return (
    <header className='bg-gray-800 text-white'>
      <div className='container mx-auto flex justify-between items-center py-4'>
        <div className='text-2xl font-bold'>AI Software Agency</div>
        <nav className='space-x-4'>
          <a href='#home' className='hover:underline'>Home</a>
          <a href='#services' className='hover:underline'>Services</a>
          <a href='#about' className='hover:underline'>About Us</a>
          <a href='#case-studies' className='hover:underline'>Case Studies</a>
          <a href='#contact' className='hover:underline'>Contact</a>
        </nav>
        <button className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'>
          Get Started
        </button>
      </div>
    </header>
  );
}

export default Header;