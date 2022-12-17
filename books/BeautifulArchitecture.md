Beautiful Architecture Snippets
===
> Oreilly

# Part I: On Architecture

## Chapter 1: What Is Architecture
> john klein, david weiss  

#### Introduction

Central to beauty is conceptual integrity -- that is, a set of abstractions
and the rules for using them thoughout the system as simply as possible.

In all disiplines, architecture provides a means for solving a common problem:
assuring that a building, or bridge, or composition, or book, or network, or
system has certain properties and behaviours when it has been built.

A good system architecture exihibits conceptual integrity; that is, it comes
equipped with a set of design rules that aid in reducing complexity and that
can be used as guidande in detailed design and in system verification.

The architecture of a computer system we define as the minimal set of
properties that determine what programs will run and what results they will be.

Architecture is a game of trade-offs -- a decision that improves one the these
characteristics often diminishes another.

In wideruse, the term "architecture" always means "unchanging deep structure".

Structures provide ways to understand the system as sets of interacting
components.

#### The role of architect

We employ an architect to assure that the design (1) meets the needs; (2) has
conceptual integrity; (3) meets legal and safety requirements.

#### What constitutes a software architecture?

Architect must make many design decisions.

External behavioral descriptions show how the product will interface with its
users, other systems, and external devices, and should take the form of
requirements. Structural descriptions show how the product is devided into
parts and the relations between those parts. Internal behavioural descriptions
are needed to describe the interface between components.

Software architectures are often presented as layered hierarchies that tend
to commingle several different structures in one diagram.

Describing the structures of an architecture as a set of views, each of which
addresses different concerns, is now accepted as a standard architecture
practice.

#### Architecture versus design

Architecture is a part of the design of the system; it highlights some details
by abstracting away from others. Architecture is thus a subset of design.

#### Creating a software architecture

The first concern of a software architect is not the functionality of the
system, but the quality concerns that needed to be satisfied.

Architecture decisions will have an impact on what kinds of changes can be
done easily and quickly and what changes will take time and be hard to do.

In the extreme case, there is no decomposition, and the system is developed as
a monolithic block of software.

Choosing one of the technologies is and architecture decision that will have
significant impact on your ability to meet cartain quality requirements.

We hope you understand by now that architecture decisions are important if your
system is going to meet its quality requirements, and what you want to pay
attention to the architecture and make these decisions intentionaly rather than
just "letting the architecture emerge".

The mind of a single user must comprehend a computer architecture. If a planned
architecture cannot be designed by a single mind, it cannot be comprehended by
one.

Fred Brooks said that conceptual integrity is the most important attribute of
an architecture.

* Functionality  
* Changeability  
* Performance  
* Capacity  
* Ecosystem  
* Modularity  
* Buildability  
* Producibility  
* Security  

#### Architectural structures

Key structural decisions divide the product into components and define the
relationships among those components.

#### Summary of structures

* Information hiding structure: "is part of", "is contained in": changeability,
modularity, buildability  
* Uses structure: "uses": producibility, ecosystem  
* Process structure: "gives work to", "gets resources from", "shares resource
with", "contained in": performance, changeability, capacity  
* Data access structure: "has access to": security, ecosystem  

#### Good architectures

Searching the web for "software architecture review checklist" returns dozens
of chechlists.

#### Beautiful architectures

Albert Einstein might say that beautiful architecture are as simple as possible,
but no simpler.

Our last example is the Unix system, which exhibits conceptual integrity, is
widely used, and has had great influence. The pipe and filters design is a
lovely abstraction that permits rapid construction of new applications.

> "Chapter1" was marked as read in Sept 2016.  

## Chapter 2: A Table of two systems: a modern-day software fable
> Pete Goodliffe  

Architecture is the art of how to waste space.

They say experience is a great teacher, but other people's experience is even
better -- if you can't learn from these projects' mistakes and successes, you
might save yourself (and your software) a lot of pain.

#### The messy metropolis

The code took a fantastically long time to learn, and there were no obvious
routes into the system. That was a warning sign. At the microlevel, looking
at individual lines, methods, and components, the code was messy and badly put
together. There was no consistency, no style, and no unifying concepts drawing
the separate parts together. That was another warning sign. ...

The metropolis was a town of planning disaster. Before you can improve a mess,
you need to udnerstand that mess, so with much effort and perseverance we pulled
together a map of the "architecture".

It was stunning. It was psychedelic.

This was the kind of system that would vex a traveling salesman.

The metropols's state of affairs was understandable (but not condonable) when
you looked at the history of the company that built it: it was a startup with
heavy pressure to get many new releases out rapidly. Delays were not tolerable
-- they would spell financial ruin. The software engineers were driven to get
code shipping as quickly as humanly possible (if not sooner). And so the code
had been thrown together in a series of mad dashes.

Poor company structure and unhealthy development processes will be reflected in
a poor software architecture.

The bad design actually encouraged further bad design to be bolted onto it --
in fact, it literally forced you to do so -- as there was no way to extend the
design in a sane way.

It's important to maintain the quality of a software design. Bad architectural
design leads to further bad architectural design.

Naturally, this made bug fixing a nightmare, which seriously affected the quality
and reliability of the software.

The health of the working relationships in your development team will feed
directly into the software design. Unhealthy releationships and inflated
egos lead to unhealthy software.

There was no bottom layer or central hub to the system. It was one monolithic
blob of software. Unnecessary coupling made low-level testing impossible.

One of the most subtle yet serious metropolis problems was duplication.

A lax and fuzzy architecture leads to individual code components that are
badly written and don't fit well together. It also leads to duplication of
code and effort.

The consequance of bad architecture is not constrained within the code. It
spills outside to affect people, teams, processes, and timescales.

The messy metropolis turned out so messy: at the very begining of the project
the team did not know what it was building.

It's important to know what you're designing before you start designing it.
If you don't know what it is and what it's supposed to do, don't design it yet.
Only design what you know you need.

No one enjoyed working with the code, and the project was heading in a
downward spiral. The lack of design had led to bad code, which led to bad
team moral and increasingly lengthy development cycles. This eventually led
to severe financial problems for the company.

---

COHESION AND COUPLING

Key qualities of software design are cohesion and coupling. We aim to design
systems with components that have:

* Strong cohesion: Cohesion is a measure of how related functionality is gathered
together and how well the parts inside a module work as a whole. Cohesion is the
glue holding a module together. Weakly cohesive modules are a sign of bad
composition. Each module must have a clearly defined role, and not be grab
bag of unrelated functionality.

* Low coupling: Coupling is a measure of the interdependency between modules
-- the amount of wiring to and from them. In the simplest designs, moduels
have less coupling so are less reliant on one another. Obviously, modules
can't be totally decoupled, or they wouldn't be working together at all.
Good software design limites the lines of communication to only those that
are absolutely necessary. These communication lines are part of what determines
the architecture.

#### Design town

Form ever follows function.

Fortunately, there was none of the interpersonal rivalry apparent in the
metropolis project, or any vying for positions of power in the team. The
members didn't know each other well beforehead and didn't know how well
we'd work together, but we were all enthused about the project and relished
the challenge.

The development process employed was extream programming (XP), which many
believe eschews design: code from the hip, and don't think too far ahead.
XP does not discourage design; it discourages work that isn't necessary (this
is the YAGNI, or You Aren't Going To Need It, principle). However, where
upfront design is required, XP requires you to do that. It also encourages
rapid prototypes (known as spikes) to flesh out and prove the validity of
designs. Both of these were very useful and contributed greatly to the final
software design.

... just some blobs on a diagram, a basic system design that could grow easily
as pieces of functionality were added. Although basic, this initial architecture
proved a solid basis for growth.

The existence of an architectural plan sometimes made the developers work harder.
The payoff for this extra effort was a much easier life later on, when maintaining
or extending the system -- there was very little cruft to trip over.

An architecture helps you to locate functionality: to add it, to modify it,
or to fix it. It provides a template for you to slot work into and a map to
navigate the system.

A clear architecture design leads to a consistent system. All decisions should
be made in the context of the architectural design.

Clear architecture helps reduce duplication of functionality.

Software architecture is not set in stone. Change it if you need to.
To be changeable, the architecture must remain simple. Resist changes
that compromise simplicity.

One of the XP principles that relly enhanced the quality of the design town
architecture was YAGNI. It encouraged us to design only the important stuff
early on, and to defer all remaining decisions untill later, when we had a
clearer picture of the actual requirements and how best to fit them into the
system. This is an immemsely powerful design approach, and quite liberating.

Defer design decisions until you have to make them. Don't make architecture
decisions when you don't know the requirements yet. Don't guess.

Architectural quality must be maintained. This can happen only when the
developers are given and take responsibility for it.

Some areas of the design town internal structure recieved quite radical
rework, and the unit tests gave us confidence that the rest of the system
had not been broken.

Having a good set of automated tests for your system allows you to make
fundamental architectureal chagnes with minimal risk. It gives you space
in which to work.

The unit tests practically enforced good structure, it forced careful
thought about each unit's interface, and ensured that the unit's APT
was meaningful and internally consistent.

Unit testing your code leads to better software designs, so design for testability.

Good projest planning leads to superior designs. Allot sufficient time to create
an architectural masterpiece -- they don't appear instantly.

A team's organization has an inevitable affect on the code it produces.

Never lose a holy curiosity. -- Albert Einstein

> Chapter 2 was marked as read in Sept 2016.  

## Chapter3 TODO
