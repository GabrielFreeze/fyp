<h1>Using Machine Learning to Investigate Potential Image Bias in News Articles</h1>

<img src="https://raw.githubusercontent.com/GabrielFreeze/fyp/main/thesis/figures/HiliGabriel_13502H_Image1.png">  </img>


<p>This project aims to develop an automatic technique to detect and analyse picture-related bias in online news articles, by integrating various machine learning models into the methodology. Picture-related bias refers to the deviation from objective reporting in media, where journalists use images to influence the perception of an event or issue.</p>
<h2>Data</h2>
<p>The project uses a dataset of real online news articles scraped from six Maltese newspapers: Times of Malta, The Shift, Malta Today, The Malta Independent, Malta Daily, and Gozo News. The dataset contains information such as article title, caption, body, image URL, and publication date.</p>
<h2>Methodology</h2>
<p>The project employs a machine-learning data-transformation pipeline to extract bias-indicative features from the news article dataset. The pipeline consists of the following steps:</p>
<ul>
<li>Named Entity Recognition (NER) Tagging: Identifies named entities such as persons, organisations, and locations in the article text using <a href="https://pypi.org/project/flair/">flair</a>.</li>
<li>Keyword Extraction: Extracts the most important topic words in the article text using <a href="https://maartengr.github.io/KeyBERT/api/keybert.html">KeyBERT</a>.</li>
<li>Sentiment Analysis: Computes the sentiment score of the article text using <a href="https://github.com/fhamborg/NewsMTSC">NewsMTSC</a>.</li>
<li>Caption Generation: Generates a synthetic caption for the article image using <a href="https://github.com/salesforce/BLIP">BLIP</a>, a state-of-the-art Vision-Language Pre-training (VLP) model that incorporates both image and text in a multi-modal fashion. The <code>BLIP-1</code> branch contains the deprecated BLIP implementation while the <code>main</code> branch contains the updated <a href="https://github.com/salesforce/LAVIS/tree/main/projects/blip2">BLIP-2</a> version</li>
<li>Synthetic Caption Similarity: Computes the cosine similarity between the synthetic caption and the article text using <a href="https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2">all-MiniLM-L6-v2</a>, a transformer-based model for text similarity.</li>
<li>Image-Text Matching: Computes the image-text matching score between the article image and the article text using BLIP.</li>
</ul>
<h2>Evaluation</h2>
<p>The project evaluates the results of the data-transformation pipeline to investigate potential picture-related bias in the online news articles. The evaluation consists of the following analyses:</p>
<cib-table-block><table><thead>
<tr>
<th><strong>Analysis</strong></th>
<th><strong>Description</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Article Similarity to Synthetic Captions</td>
<td>Compares the similarity between the article title, caption, and body to the synthetic caption generated by BLIP, and visualises the results using maxdiff barcharts and scatter plots.</td>
</tr>
<tr>
<td>Article Similarity to Images</td>
<td>Compares the similarity between the article title, caption, and body to the article image, and visualises the results using barcharts and density plots.</td>
</tr>
<tr>
<td>Image-Text Similarity against Article Sentiment</td>
<td>Examines the relationship between the image-text similarity score and the article sentiment score, and visualises the results using stacked barcharts.</td>
</tr>
<tr>
<td>Application in Media Bias Research</td>
<td>Demonstrates how the proposed technique can be used to fact-check older studies, as well as to alleviate some of the manual work performed by researchers in picture-related media bias studies.</td>
</tr>
</tbody>
</table>
  
<h2>Results</h2>  
<table>
  <p> A table of the aggregated mean results of the demonstration. All values
represent a percentage. ∗ denotes that Caption metrics were not included while
calculating the mean.</p>
  <tr>
    <th>Newspaper</th>
    <th>Synthetic Caption Similarity</th>
    <th>Image Similarity</th>
    <th>Positive Sent.</th>
    <th>Neutral Sent.</th>
    <th>Negative Sent.</th>
  </tr>
  <tr>
    <td>Times of Malta</td>
    <td>15.99</td>
    <td>30.99</td>
    <td>13.87</td>
    <td>65.55</td>
    <td>20.58</td>
  </tr>
  <tr>
    <td>The Shift</td>
    <td>9.27</td>
    <td>20.78</td>
    <td>11.71</td>
    <td>62.68</td>
    <td>25.60</td>
  </tr>
  <tr>
    <td>Malta Today</td>
    <td>10.80</td>
    <td>24.15</td>
    <td>16.79</td>
    <td>67.03</td>
    <td>16.18</td>
  </tr>
  <tr>
    <td>Malta Independent*</td>
    <td>10.96</td>
    <td>29.92</td>
    <td>21.27</td>
    <td>62.56</td>
    <td>16.17</td>
  </tr>
  <tr>
    <td>Malta Daily∗</td>
    <td>13.46</td>
    <td>50.79</td>
    <td>28.81</td>
    <td>58.72</td>
    <td>12.47</td>
  </tr>
  <tr>
    <td>Gozo News∗</td>
    <td>13.58</td>
    <td>38.76</td>
    <td>25.17</td>
    <td>69.46</td>
    <td>5.37</td>
  </tr>
</table>



<h2>Conclusion</h2>
<p>The project demonstrates a novel machine-learning technique to investigate picture-related bias in online news articles, by utilising various state-of-the-art models and methods. The project shows promising results for the adoption of this technique by media bias researchers, as well as for the empowerment of journalists and news readers in analysing the potential presence of picture-related bias. The project also suggests some future improvements and extensions for the technique.</p>


<h3>Contact</h3>
gabriel.hili@um.edu.mt

<h3>Cite this work</h3>
<pre>
  @mastersthesis{hili2023using,
  title={Using machine learning to investigate potential image bias in news articles},
  author={Hili, Gabriel},
  type={{B.S.} thesis},
  year={2023},
  school={University of Malta}
}
</pre>

