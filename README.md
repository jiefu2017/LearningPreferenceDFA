# Learning Preference deterministic finite-state automaton from pairwise comparisons

## This project is designed to learn a Preference deterministic finite-state automaton from pairwise comparisons of words.

## Table of Contents
- [aaply](#AALpy is a light-weight automata learning library written in Python. Revised for learning PDFA)
- [Learning](#PreferenceSample.py, RPNIMooreBased.py are the main algorithms. Samplier.py is to generate samples from a given PDFA.)
- [Learning_CaseStudies] (#Two case studies used in the manuscript.)
- [PDFA_JSON](#Saved learned pdfa using .json file)
- [Utility] (#Auxilary functions)
- [Contributing](#contributing)


<!-- GETTING STARTED -->
## Getting Started
1. Clone the repo
   ```sh
   git clone    ```
### Prerequisites
* jsonpickle: https://jsonpickle.github.io/
* automata-lib: https://pypi.org/project/automata-lib/
* graphviz: https://graphviz.org/

<!-- USAGE EXAMPLES -->

The repository contains the following two classes of case study:
- Case study 1 [Running example in the paper]: The first case study is a synthetic example with 3 states and 2 symbols. The PDFA is learned from 1000 samples. 
- Case study 2 [BeeRobot]: The second case study is a real-world example from the BeeRobot dataset. The PDFA is learned from 1000 samples.

For both case studies 1 and 2, the ground truth preference DFAs are provided and used for generating the sample sets for multiple experiments. The following functions are implemented:
1. compute the set of shortest prefixes and the nucleus. 
2. determine if the given sample is characteristic or not.
3. compute the closure of a given sample set.
4. Use the RPNIMooreBased algorithm to learn the PDFA from the sample set and determine if it is equivalent to the ground truth PDFA.

Another example, ex2.py, showcases the experiment when no ground truth PDFA is provided and a PDFA is learned from the sample set.

Please refer to the manuscript for more details on the case studies and the experiments.


~~<!-- CONTRIBUTING -->
## Contributing

Contributions are what~~ make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Top contributors:
TODO: Hazhar add your information
<a href="https://github.com/github_username/repo_name/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>


TODO: Jie Fu, University of Florida
<a href="https://github.com/jiefu2017">
  <img src="https://contrib.rocks/image?repo=github_username/repo_name" alt="contrib.rocks image" />
</a>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact
Hazhar Rahmani - hrahmani@missouristate.edu

Jie Fu - fujie@ufl.edu

Project Link: 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
"This material is based upon work supported by the Air Force Office of Scientific Research under award
number FA9550-21-1-0085."

"Any opinions, findings, and conclusions or recommendations expressed in this material are those of the
author(s) and do not necessarily reflect the views of the United States Air Force."

<p align="right">(<a href="#readme-top">back to top</a>)</p>
