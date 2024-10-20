import React from 'react';

function AboutUs() {
  return (
    <section id='about' className='py-20 bg-gray-100'>
      <div className='container mx-auto flex flex-col md:flex-row items-center'>
        <div className='w-full md:w-1/2 mb-10 md:mb-0'>
          <img src='https://picsum.photos/id/237/200/300' alt='About Us' className='w-full rounded-lg shadow-lg' />
        </div>
        <div className='w-full md:w-1/2 md:pl-10'>
          <h2 className='text-3xl font-bold mb-4'>About Us</h2>
          <p className='mb-4'>Our mission is to empower businesses by transforming innovative ideas into intelligent AI-driven solutions.</p>
          <p className='mb-4'>We envision a future where AI seamlessly integrates with everyday operations, driving efficiency and growth.</p>
          <ul className='list-disc list-inside'>
            <li>Expert team</li>
            <li>Cutting-edge technology</li>
            <li>Tailored solutions</li>
          </ul>
        </div>
      </div>
    </section>
  );
}

export default AboutUs;
