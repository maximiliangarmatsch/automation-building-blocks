import React from 'react';

function CaseStudies() {
  return (
    <section id='case-studies' className='py-20 bg-gray-100'>
      <div className='container mx-auto flex flex-col md:flex-row items-center'>
        <div className='w-full md:w-1/2 mb-10 md:mb-0'>
          <img src='https://picsum.photos/id/237/200/300' alt='Case Studies' className='w-full rounded-lg shadow-lg' />
        </div>
        <div className='w-full md:w-1/2 md:pl-10'>
          <h2 className='text-3xl font-bold mb-4'>Case Studies</h2>
          <p className='mb-4'>Discover how our AI solutions transformed businesses.</p>
          <a href='#read-more' className='text-blue-600 hover:underline'>Read our success stories</a>
        </div>
      </div>
    </section>
  );
}

export default CaseStudies;
