import Head from 'next/head'
import React from 'react'
import { withPageAuthRequired } from "@auth0/nextjs-auth0/client";




const About = ({ user, error, isLoading }) => {
  const title = "Documentation - Collections Transformer (TaNC UAL)"

  return (
    <>
      <Head>
        <title>{title}</title>
      </Head>
      <main>
        <div className="container">

            <h1>Frequently Asked Questions (FAQ)</h1>
            <hr/>

            <div style={{
                width: '100%',
                margin: '2rem 0',
                lineHeight: '1.6',
                padding: '2rem',
                border: '3px solid black',
                borderRadius: '12px',
                backgroundColor: '#f5f5f5'
            }}>
            
            <h3><u>Glossary</u></h3>
            <br></br>

            <ul>
              <li><strong>Analytical Model:</strong> Is a Large Language Model-powered system that detects specific patterns or symbols within datasets.</li>
              <li><strong>Dataset:</strong> A collection of images or texts that are to be analysed.</li>
              <li><strong>Your Workspace:</strong> The database of models, datasets, analytical tasks and annotations that are created by users.</li>
              <li><strong>Analytical Task:</strong> LLM-powered analysis performed by the user on the available datasets.</li>
            </ul>

            <br></br>

            <h3><u>FAQ</u></h3>
            <br></br>

            <ul>
              <li><strong>What can this platform do?</strong> This platform allows users to create AI-powered analysers (entitled Analytical Models) that assist in detecting patterns and symbols within datasets. This platform allows to input datasets of arbitrary size and create analysis on their elements given a few examples. Each user has a workspace where they can manage and analyse data, and visit previous interactions with the system (entitled Analytical Tasks).</li>
              <br/>
              <li><strong>What does this platform not do?</strong> This platform does not allow to change the datasets themselves or create media from them. It is a tool to assist in the analysis undertaken by professionals in the GLAM sector (Galleries, Libraries, Archives, and Museums), allowing to identify negative or positive patterns in data, annotate specific considerations over the dataset and use that interaction to inform future ones. It is also possible to download a spreadsheet file from each analysis, containing the results and IDs of the items analysed. </li>
              <br/>
              <li><strong>What is a model?</strong> A model is a representation of data that we can use. When we refer to models in the Collections Transformer, they are Analytical Models, that allow to detect specific patterns or symbols within datasets, users can improve them through annotations and by providing examples. Please refer to the <a href="/newmodel" style={{ textDecoration: 'underline', color: '#000000' }}>New Model</a> page for more information.</li>
              <br/>
              <li><strong>What is a dataset?</strong> A dataset is a collection of images or texts that are to be analysed. Please refer to the <a href="/uploaddataset" style={{ textDecoration: 'underline', color: '#000000' }}>New Dataset</a> page to upload a dataset to the platform.</li>
              <br/>
              <li><strong>What is a workspace?</strong> A workspace is the user's database of models and datasets that are uploaded by users. Please refer to the <a href="/ecosystem" style={{ textDecoration: 'underline', color: '#000000' }}>Workspace</a> page for more information.</li>
              <br/>
              <li><strong>The datasets uploaded are private?</strong> Yes, the datasets uploaded are private and only accessible to the user who uploaded them. However, it is possible to make them public and accessible to other users.</li>
              <br/>
              <li><strong>Are the datasets analysed privately?</strong> Yes, each analysis is private to the current developer account and not shared online. It is important to acknowledge that this platform uses OpenAI API and inference is not done locally on the user's device, this makes analysis not always anomyous but following adjacent privacy laws.</li>
            </ul>

            <br></br>


            <h3><u>Getting Started</u></h3>

            <br></br>


            <h4><u>How to Create a New Analytical Model</u></h4>
            <br></br>

            <p style={{ marginBottom: '1rem' }}>
              To create a new Analytical Model, go to the <a href="/newmodel" style={{ textDecoration: 'underline', color: '#000000' }}>New Model</a> page. There, you will find a form where you can enter the details for your model. Once created, your model will appear in your workspace and can be used to analyse your datasets.
            </p>
            

            <ul>
              <li><strong>Name:</strong> Give your model a descriptive name (e.g., "Red_Symbols_Detector").</li>
              <li><strong>Task Description:</strong> Clearly describe what you want the model to do (e.g., "Identify artworks that contain red circular symbols.").</li>
              <li><strong>Labelling Guide:</strong> Provide instructions or criteria for what counts as a positive or negative example.</li>
              <li><strong>Type:</strong> Choose the type of analysis (e.g., binary, score, or opinion). Binary outputs a True or False answer; Score outputs a number between 0 and 5, and Opinion outputs a text explanation as analysis (number of sentences to define in the interface).</li>
              <li><strong>Examples:</strong> Select a few items from your dataset and label them as positive or negative examples to help condition the model's inference.</li>
            </ul>

            <p>
              <strong>Tip:</strong> The more clear and specific your examples and instructions, the better your model will perform!
            </p>

            <br></br>

            <h4><u>Example Walkthrough: Image Analyser - True or False</u></h4>
            <br></br>

            <p style={{ marginBottom: '1rem' }}>
              Here is an example of how to fill out the form to create an Analytical Model that analyses images to determine if a painting is considered abstract art or visually abstracting natural forms.
            </p>

            <ul>
              <li>
                <strong>Overview:</strong> This model will analyse paintings and decide if they are examples of abstract art, providing a reason for the decision. It is especially useful for distinguishing between abstract and non-abstract works based on visual structure and relevant art movements.
              </li>
              <li>
                <strong>Name:</strong> <code>model_1</code>
              </li>
              <li>
                <strong>Task Description:</strong> <code>Identify carefully if a painting is considered abstract art. Focus on the structure of images and if it is abstracting natural forms.</code>
              </li>
              <li>
                <strong>Label Type:</strong> <code>True or False</code>
                <br />
              </li>
              <li>
                <strong>Labelling Guide:</strong> <code>Analyse if the submitted paintings have specific symbols or elements from specific abstract art movements. The examples chosen, the positive label is an abstract painting and the second label is not</code>
                <br />
              </li>
              <li>

                <strong>Positive Example:</strong> Tate Image (MMM) example.

              </li>
              <li>

                <strong>Negative Example:</strong> Tate Image (MMM) example.

              </li>
              
            </ul>
            <p>
              <strong>Tip:</strong> When providing examples, make sure to include both clear positive and negative cases, and use the labelling guide to explain your reasoning. This helps the model understand what to look for in new images! The labels are done by clicking on the grid when selecting the examples. 
            </p>


            <img src="/analysis_1.png" alt="Analysis 1" style={{ width: '60%', margin: '1rem 0', border: '3px solid black'}} />

            <p>
              <strong>It is possible that the model fails to detect the pattern in specific images.</strong> In this case, we can say that forms can be abstracted visually in many ways, and not necessarily belong to any specific art movement or expression of abstraction, so we recommend to always annotate the analysis.
            </p>

            <br></br>

            <h4><u>Example Walkthrough: Text Analyser - Score</u></h4>
            <br></br>

            <p style={{ marginBottom: '1rem' }}>
              Here is an example of how to fill out the form to create an Analytical Model that analyses texts (descriptions of artworks) to determine if the language used is appropriate for a given problem.
            </p>

            <ul>
              <li>
                <strong>Overview:</strong> This model will analyse painting descriptions and help decide if the description is appropriate for the collection. It is especially useful for distinguishing acceptable or not acceptable descriptions.
              </li>
              <li>
                <strong>Name:</strong> <code>model_2</code>
              </li>
              <li>
                <strong>Task Description:</strong> <code>Identify carefully if a painting description is appropriate for the collection. Focus on the language used and the content of the description.</code>
              </li>
              <li>
                <strong>Label Type:</strong> <code>Score</code>
                <br />
              </li>
              <li>
                <strong>Labelling Guide:</strong> <code>Analyse if the submitted descriptions are appropriate for the collection. The examples chosen, the positive label is an appropriate description and the second label is not. Detect words such as "crippled" or "disabled" and related terms.</code>
                <br />
              </li>
              <li>

                <strong>Positive Example:</strong> Tate Text (MMM) example.

              </li>
              <li>

                <strong>Negative Example:</strong> Tate Text (MMM) example.

              </li>
              
            </ul>
            
            
              

            </div>
        </div>
      </main>
    </>
  )
}

export default withPageAuthRequired(About)

