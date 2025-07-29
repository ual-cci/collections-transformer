import Head from 'next/head'
import React, {useEffect, useState} from 'react'

import { useUser, withPageAuthRequired } from "@auth0/nextjs-auth0/client";
import Link from 'next/link';


const Home = ({user, error, isLoading}) => {

    const title = "Collections Transformer (TaNC UAL)"

    return (

      <>
      <Head>
        <title>{title}</title>
      </Head>
        <main>
            <div className="container">
              <h1>Collections Transformer</h1>
              <hr/>

              <div className='feature-box intro'>
                <div>
                  
                  <u><strong>Welcome {user.name === user.email ? user.nickname : user.name}</strong>!</u> <br></br><br></br>
                  
                  This platform allows users to create AI-powered models and analysis to assist in detecting patterns within collections and other datasets. Analytical Models are created for analysis tied to each user's account, and they allow to label and identify patterns in a collection. A few examples and a description is what is needed, and if the model fails doing so, the human can label and record the analysis. With a small set of carefully curated information (texts and images), each analysis is created and managed in the workspace.

                </div>
                
              
              </div>

            </div>

            
        </main>
      </>
  )
}

export default withPageAuthRequired(Home)
