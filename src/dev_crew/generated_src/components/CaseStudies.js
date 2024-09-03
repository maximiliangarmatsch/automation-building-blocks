
import React from 'react';

const CaseStudies = () => {
  return (
    <section className='bg-white py-20'>
      <div className='container mx-auto'>
        <h2 className='text-3xl font-bold text-center mb-12'>Case Studies</h2>
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'>
          <div className='bg-gray-100 p-6 rounded-lg'>
            <h3 className='text-xl font-bold mb-2'>[Project Title]</h3>
            <p className='mb-4'>A brief description of how our AI solutions transformed a client's business.</p>
            <a href='#' className='text-blue-500 hover:underline'>Read More</a>
          </div>
          <div className='bg-gray-100 p-6 rounded-lg'>
            <h3 className='text-xl font-bold mb-2'>[Project Title]</h3>
            <p className='mb-4'>A brief description of how our AI solutions solved a complex problem for a client.</p>
            <a href='#' className='text-blue-500 hover:underline'>Read More</a>
          </div>
          <div className='bg-gray-100 p-6 rounded-lg'>
            <h3 className='text-xl font-bold mb-2'>[Project Title]</h3>
            <p className='mb-4'>A brief description of how our AI solutions enhanced operational efficiency for a client.</p>
            <a href='#' className='text-blue-500 hover:underline'>Read More</a>
          </div>
        </div>
      </div>
    </section>
  );
}

export default CaseStudies;