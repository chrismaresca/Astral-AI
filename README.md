
---

<a id="readme-top"></a>

<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<!--
*** Thanks for checking out Astral AI. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING!
-->

<!-- PROJECT SHIELDS -->
<div align="center">
  
<!-- [![Forks][forks-shield]][forks-url] [![Stargazers][stars-shield]][stars-url] [![Issues][issues-shield]][issues-url] [![LinkedIn][linkedin-shield]][linkedin-url] -->

</div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/chrismaresca/Astral-AI">
    <img src="public/white-bg.png" alt="Astral AI Logo" width="80" height="80">
  </a>

  <h3 align="center">Astral AI</h3>
  <p align="center">
    <a href="https://github.com/chrismaresca/Astral-AI/blob/main/LICENSE">
      <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="MIT License">
    </a>
  </p>

  <p align="center">
    Astral is an open-source framework for AI engineers that abstracts away the complexity and friction of working across multiple model providers.
    <br />
    <a href="https://www.useastral.dev/docs/getting-started/installation"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://www.useastral.dev">View Demo</a>
    &middot;
    <a href="https://www.useastral.dev">Home Page</a>
    &middot;
    <!-- <a href="https://github.com/chrismaresca/Astral-AI/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot; -->
    <a href="https://www.useastral.dev/contact-us">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#why-astral">Why Astral?</a></li>
        <li><a href="#our-vision">Our Vision</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#join-the-astral-community">Join the Astral Community!</a></li>
        <li><a href="#getting-started-contributing">Getting Started Contributing</a></li>
        <li><a href="#examples">Examples</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#found-an-issue">Found an issue?</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#inspiration">Inspiration</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

[![Astral AI Homepage](public/astral-homepage.png)](https://www.useastral.dev)

Astral is an open-source framework for AI engineers that abstracts away the complexity and friction of working across multiple model providers.

### Why Astral?

Astral comes from Late Latin, meaning *of, relating to, or coming from the stars.* The stars have long symbolized discovery, exploration, and the interconnected systems that shape our universe.

AI capabilities such as completions, embeddings, image and video generation, real-time audio, and speech-to-text are essential building blocks of the next industrial revolution. But today, these capabilities remain fragmented, locked behind provider-specific implementations that slow innovation.

**Astral changes that.** By seamlessly integrating these powerful resources into a cohesive, universal framework, **Astral enables engineers to build at the speed of discovery.** We empower innovators to transcend today's limitations, guiding them toward a new frontier of human-AI interaction—unlocking infinite possibilities.

### Our Vision

Astral provides a type-safe, unified interface that developers can use to integrate across providers and resources, including completions, embeddings, real-time audio, and speech-to-text, without being locked into any single provider. By eliminating provider-specific inconsistencies, Astral enables engineers to build, scale, and iterate on AI-driven applications with greater speed and efficiency.

Looking ahead, we envision building enterprise solutions on top of Astral's core open-source SDK, including prompt versioning, template management, workflow automation, and evaluation frameworks that work across providers and organizations.

Our goal is to become the go-to framework for building AI applications, from agentic systems to enterprise workflows, while remaining a thin, high-performance layer that avoids the inefficiencies of heavier frameworks.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ### Built With

- [Python](https://www.python.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/) -->


<!-- <p align="right">(<a href="#readme-top">back to top</a>)</p> -->

<!-- GETTING STARTED -->

## Getting Started

This section shows you how to get a local copy up and running. For a more structured overview, see our docs here: [Astral Documentation](https://www.useastral.dev/docs/)

### Prerequisites

- Requires Python **>=3.12**
- Authentication credentials for whatever model providers you're interested in using (i.e API key for OpenAI, API key for Anthropic, etc)

### 🌌 Join the Astral Community!
<a id="join-the-astral-community"></a>

Before diving in, make sure to:

1. **⭐️ Star the Repository!**  
  Show your support by starring the [repo](https://github.com/chrismaresca/Astral-AI)—it helps new builders discover us and expands our community!

2. **💬 Join our Discord Community:**  
   Hop into our vibrant [Discord community](https://discord.gg/SPNqRrPR) to connect with fellow contributors, brainstorm ideas, ask questions, or just hang out! It's the best place to stay updated on everything Astral.

3. **🐦 Follow me on X:**  
   Stay updated with the latest news and updates by following me on [X](https://x.com/thechrismaresca).

   Thanks for helping shape the future of Astral—we can't wait to see what you build!

### **🚀 Getting Started Contributing**
<a id="getting-started-contributing"></a>

Ready to build something awesome? Follow these steps:

1. **🍴 Fork and Clone:**  
   Begin by forking the repository to your GitHub account and cloning your fork locally:
   ```bash
   # First, fork the repository on GitHub, then clone your fork
   git clone https://github.com/chrismaresca/Astral-AI.git
   cd Astral-AI
   ```

2. **⚙️ Set Up Development Environment:**  
   We utilize [**UV**](https://docs.astral.sh/uv/)—a high-performance Python package and project manager built with Rust—to simplify setup.
   ```bash
   # Execute the following command to create a virtual environment and install all dependencies.
   uv sync
   ```

3. **📚 Refer to Quick Start Guide:**  
   Access our developer quick start guide here: [Quick Start](https://www.useastral.dev/docs/getting-started/quick-start)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### **🔍 Examples**
<a id="examples"></a>

Dive into our demos and guides to get a hands-on experience: [Demos](https://www.useastral.dev/docs/guides/quick-start)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## **🛤️ Roadmap**
<a id="roadmap"></a>

See our vision for the future of AI engineering: [Future Vision](https://www.useastral.dev/resources/future-vision) 🌌

See the [open issues](https://github.com/chrismaresca/Astral-AI/issues) for a full list of proposed features (and known issues) 📝. 

If you found a bug or have a feature request? Check out our [Found an issue?](#found-an-issue) section to learn how to contribute.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTRIBUTING -->

## **🤝 Contributing**
<a id="contributing"></a>

Your contributions are what make Astral shine! For more information, see the [CONTRIBUTING.md](CONTRIBUTING.md) file. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- Found an issue?  -->
## 🐛 Found an issue?
<a id="found-an-issue"></a>

If you have found an issue with our documentation, please [create an issue](https://github.com/chrismaresca/Astral-AI/issues).

If it's a quick fix, such as a misspelled word or a broken link, feel free to skip creating an issue.
Go ahead and create a [pull request](https://github.com/chrismaresca/Astral-AI/pulls) with the solution. 🚀

Or you can [contact Chris](#contact) directly if you prefer.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- LICENSE -->

## License

Distributed under the MIT License. See the [LICENSE](LICENSE) file for more information.


<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->


<!-- CONTACT -->

## Contact

<div align="center">
  <img src="https://github.com/chrismaresca.png" width="100" height="100" style="border-radius:50%">
  <h3>Chris Maresca</h3>
  
  [![Twitter](https://img.shields.io/badge/Twitter-%40TheChrisMaresca-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://x.com/TheChrisMaresca)
  [![LinkedIn](https://img.shields.io/badge/LinkedIn-Chris%20Maresca-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/chris-maresca/)
  [![Email](https://img.shields.io/badge/Email-chris%40useastral.dev-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:chris@useastral.dev)
  
</div>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Inspiration

- [Building Effective Agents – Anthropic](https://www.anthropic.com/engineering/building-effective-agents) - Insights on creating autonomous AI systems that can effectively solve complex tasks
- [Aligning Language Models To Follow Instructions – OpenAI](https://openai.com/blog/instruction-following) - Best practices for crafting effective prompts
- [Linear – In artfully blending software and design](https://linear.app/) - Inspiration for thoughtful product design and user experience
- [Steve Jobs on Changing the World](https://www.youtube.com/watch?v=kYfNvmF0Bqw) - "When you grow up you tend to get told the world is the way it is... life changes when you realize one simple truth: Everything around you that you call life was made up by people that were no smarter than you."
- My approach to software development has been profoundly shaped by the philosophical and poetic insights of Charles Bukowski:
  - [Style - Charles Bukowski](https://www.goodreads.com/quotes/150224-style-is-the-answer-to-everything-a-fresh-way-to) - "Style is the answer to everything..."
  - [So You Want To Be a Writer - Charles Bukowski](https://allpoetry.com/so-you-want-to-be-a-writer) - On authentic creation and finding your voice

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge  
[contributors-url]: https://github.com/chrismaresca/Astral-AI/graphs/contributors  
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge  
[forks-url]: https://github.com/chrismaresca/Astral-AI/network/members  
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge  
[stars-url]: https://github.com/chrismaresca/Astral-AI/stargazers  
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge  
[issues-url]: https://github.com/chrismaresca/Astral-AI/issues  
[license-shield]: https://img.shields.io/badge/License-MIT-yellow.svg
[license-url]: https://github.com/chrismaresca/Astral-AI/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555  
[linkedin-url]: https://www.linkedin.com/in/chris-maresca/  
[product-screenshot]: images/screenshot.png

[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white  
[Next-url]: https://nextjs.org/  
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB  
[React-url]: https://reactjs.org/  
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D  
[Vue-url]: https://vuejs.org/  
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white  
[Angular-url]: https://angular.io/  
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00  
[Svelte-url]: https://svelte.dev/  
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white  
[Laravel-url]: https://laravel.com  
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white  
[Bootstrap-url]: https://getbootstrap.com  
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white  
[JQuery-url]: https://jquery.com

---
