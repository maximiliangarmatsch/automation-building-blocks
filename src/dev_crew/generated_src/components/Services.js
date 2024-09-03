
import React from 'react';

const Services = () => {
  return (
    <section className='bg-white py-20'>
      <div className='container mx-auto'>
        <h2 className='text-3xl font-bold text-center mb-12'>Our Services</h2>
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8'>
          <div className='bg-gray-100 p-6 rounded-lg text-center'>
            <h3 className='text-xl font-bold mb-2'>Custom AI Development</h3>
            <p className='mb-4'>Tailored AI solutions designed to meet the unique challenges of your business.</p>
            <a href='#' className='text-blue-500 hover:underline'>Learn More</a>
          </div>
          <div className='bg-gray-100 p-6 rounded-lg text-center'>
            <h3 className='text-xl font-bold mb-2'>Data Analysis & Visualization</h3>
            <p className='mb-4'>Transform your data into actionable insights with our advanced data analysis and visualization techniques.</p>
            <a href='#' className='text-blue-500 hover:underline'>Learn More</a>
          </div>
          <div className='bg-gray-100 p-6 rounded-lg text-center'>
            <h3 className='text-xl font-bold mb-2'>Machine Learning Models</h3>
            <p className='mb-4'>Develop and deploy state-of-the-art machine learning models to drive efficiency and innovation.</p>
            <a href='#' className='text-blue-500 hover:underline'>Learn More</a>
          </div>
          <div className='bg-gray-100 p-6 rounded-lg text-center'>
            <h3 className='text-xl font-bold mb-2'>AI Consultation</h3>
            <p className='mb-4'>Expert guidance to help you navigate the complexities of AI and make informed decisions.</p>
            <a href='#' className='text-blue-500 hover:underline'>Learn More</a>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Services;