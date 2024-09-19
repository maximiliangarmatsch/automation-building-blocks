import React from 'react';

function Services() {
  return (
    <section id='services' className='py-20'>
      <div className='container mx-auto text-center'>
        <h2 className='text-3xl font-bold mb-10'>Our Services</h2>
        <div className='grid grid-cols-1 md:grid-cols-3 gap-8'>
          <div className='p-6 bg-white rounded-lg shadow-lg'>
            <div className='text-mint-600 mb-4'>
              <svg className='w-12 h-12 mx-auto' fill='none' stroke='currentColor' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><path strokeLinecap='round' strokeLinejoin='round' strokeWidth='2' d='M12 8c.598 0 1.175-.13 1.68-.367C14.292 8.645 15.065 9 16 9c1.656 0 3-1.343 3-3s-1.344-3-3-3c-.932 0-1.704.355-2.32.927C12.826 3.13 12.25 3 12 3c-.598 0-1.175.13-1.68.367C9.708 3.355 8.935 3 8 3c-1.656 0-3 1.343-3 3s1.344 3 3 3c.932 0 1.704-.355 2.32-.927C10.826 7.87 11.402 8 12 8zM12 12c-.598 0-1.175.13-1.68.367-.616-.572-1.388-.927-2.32-.927-1.656 0-3 1.343-3 3s1.344 3 3 3c.932 0 1.704-.355 2.32-.927.505.237 1.082.367 1.68.367s1.175-.13 1.68-.367C14.292 17.645 15.065 18 16 18c1.656 0 3-1.343 3-3s-1.344-3-3-3c-.932 0-1.704.355-2.32.927-.505-.237-1.082-.367-1.68-.367zm0 4c-.598 0-1.175.13-1.68.367-.616-.572-1.388-.927-2.32-.927-1.656 0-3 1.343-3 3s1.344 3 3 3c.932 0 1.704-.355 2.32-.927.505.237 1.082.367 1.68.367s1.175-.13 1.68-.367c.616.572 1.388.927 2.32.927 1.656 0 3-1.343 3-3s-1.344-3-3-3c-.932 0-1.704.355-2.32.927-.505-.237-1.082-.367-1.68-.367zm0-8c-.598 0-1.175.13-1.68.367-.616-.572-1.388-.927-2.32-.927-1.656 0-3 1.343-3 3s1.344 3 3 3c.932 0 1.704-.355 2.32-.927.505.237 1.082.367 1.68.367s1.175-.13 1.68-.367c.616.572 1.388.927 2.32.927 1.656 0 3-1.343 3-3s-1.344-3-3-3c-.932 0-1.704.355-2.32.927-.505-.237-1.082-.367-1.68-.367z'></path></svg>
            </div>
            <h3 className='text-xl font-bold mb-2'>AI Consulting</h3>
            <p>Expert guidance to help you leverage AI for business growth.</p>
          </div>
          <div className='p-6 bg-white rounded-lg shadow-lg'>
            <div className='text-mint-600 mb-4'>
              <svg className='w-12 h-12 mx-auto' fill='none' stroke='currentColor' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><path strokeLinecap='round' strokeLinejoin='round' strokeWidth='2' d='M10.25 4.75L7 7.5m14 0l-3.25-2.75M5 11h14M5 19h14M5 15h14m-7 4v-4m0 4v-4m0-4v-4m0 4v-4'></path></svg>
            </div>
            <h3 className='text-xl font-bold mb-2'>Custom AI Development</h3>
            <p>Tailored AI solutions designed to meet your unique needs.</p>
          </div>
          <div className='p-6 bg-white rounded-lg shadow-lg'>
            <div className='text-mint-600 mb-4'>
              <svg className='w-12 h-12 mx-auto' fill='none' stroke='currentColor' viewBox='0 0 24 24' xmlns='http://www.w3.org/2000/svg'><path strokeLinecap='round' strokeLinejoin='round' strokeWidth='2' d='M12 8c.598 0 1.175-.13 1.68-.367C14.292 8.645 15.065 9 16 9c1.656 0 3-1.343 3-3s-1.344-3-3-3c-.932 0-1.704.355-2.32.927C12.826 3.13 12.25 3 12 3c-.598 0-1.175.13-1.68.367C9.708 3.355 8.935 3 8 3c-1.656 0-3 1.343-3 3s1.344 3 3 3c.932 0 1.704-.355 2.32-.927C10.826 7.87 11.402 8 12 8zM12 12c-.598 0-1.175.13-1.68.367-.616-.572-1.388-.927-2.32-.927-1.656 0-3 1.343-3 3s1.344 3 3 3c.932 0 1.704-.355 2.32-.927.505.237 1.082.367 1.68.367s1.175-.13 1.68-.367C14.292 17.645 15.065 18 16 18c1.656 0 3-1.343 3-3s-1.344-3-3-3c-.932 0-1.704.355-2.32.927-.505-.237-1.082-.367-1.68-.367zm0 4c-.598 0-1.175.13-1.68.367-.616-.572-1.388-.927-2.32-.927-1.656 0-3 1.343-3 3s1.344 3 3 3c.932 0 1.704-.355 2.32-.927.505.237 1.082.367 1.68.367s1.175-.13 1.68-.367c.616.572 1.388.927 2.32.927 1.656 0 3-1.343 3-3s-1.344-3-3-3c-.932 0-1.704.355-2.32.927-.505-.237-1.082-.367-1.68-.367zm0-8c-.598 0-1.175.13-1.68.367-.616-.572-1.388-.927-2.32-.927-1.656 0-3 1.343-3 3s1.344 3 3 3c.932 0 1.704-.355 2.32-.927.505.237 1.082.367 1.68.367s1.175-.13 1.68-.367c.616.572 1.388.927 2.32.927 1.656 0 3-1.343 3-3s-1.344-3-3-3c-.932 0-1.704.355-2.32.927-.505-.237-1.082-.367-1.68-.367z'></path></svg>
            </div>
            <h3 className='text-xl font-bold mb-2'>AI Implementation</h3>
            <p>Seamless integration of AI technologies into your existing systems.</p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Services;
