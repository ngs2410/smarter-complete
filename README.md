Smarter Complete
================

Apply machine learning and language processing to create smarter auto complete
suggestions when programming

Goals
-----

This is an experimental project with the following goal(s):

1. To determine whether machine learning and language processing techniques
can be used to improve programmer efficiency by automatically identifying
frequently repeated code snippets from a large body of code and
(intelligently) proposing those snippets in typical auto-complete situations.
2. There's only one goal right now.

Target
------

The initial target editor is Sublime Text. Sublime Text is a popular editor
that exposes hooks into the auto-complete mechanism and supports statically
defined code snippets. Those hooks are easiest to implement in Python. The
target language for auto-completion is Javascript. Javascript has been
selected as it is a popular language, syntactically relatively simple but (to
the author at least) verbose, repetitive and ripe for rich auto-complete
suggestions.

Motivation
----------

Several factors are motivating this experiment.

1. Anecdotally, the author estimates that 99.5-99.9% of the time spent
programming is wasteful and inefficient. The mind's ability to imagine the
solution to a programming problem or write the next line is probably only
0.5-0.1% of the time it takes to actually transcribe, correct and test the
code. This only gets worse as programmers have to work with more complex
systems, multiple languages, reference documentation more frequently etc.

2. Recently, the author crafted a very large body of Javascript code in a
node.js based RESTful API. While modern frameworks allow for a much higher
level of abstraction, the act of transcribing code line by line was very
reminiscient of programming BASIC on a Commodore PET in 1979. Depressing.

3. While this is not true for all programmers, a couple of friends have
identified that a lot of "average" programming these days involves simply
copying and pasting code from one place (another file or Stack Overflow) to
another, adjusting some variables and moving on. Similarly depressing.

4. I was looking for a project to try out some new (to me) technologies.

Quantification
--------------

It's important to be able to measure the usefulness of this experiment. We're
going to measure usefulness in terms of getting the code that we expect in the
shortest possible time, or the fewest number of keypresses.

The code here represents a fragment that I felt like I wrote several times
each day for a period of two years:

```javascript
var async = require('async')
	, _ = require('underscore')
	;

function Target () {
	var self = this;
	self.invocations = 0;
}

Target.prototype.fibonacci = function(n, cb) {
	var self = this;
	self.invocations++;

	if (n < 1 || n > 100) return cb(new Error('Number out of range'));
	if (n === 1 || n === 2) return cb(null, 1);

	async.auto({
		first : function (firstCallback) {
			self.fibonacci(n-1, firstCallback);
		},
		second : function (secondCallback) {
			self.fibonacci(n-2, secondCallback);
		}
	}, function (err, r) {
		if (err) return cb(err);
		cb(null, r.first + r.second);
	});
};

var t = new Target(), n = 10;
t.fibonacci(n, function (err, r) {
	if (err) {
		console.log('Error', err);
	} else {
		console.log('Fibonnaci of', n, '=', r);
	}
});
```

That's ~761 bytes which we can assume is 761 keypresses if we give ourselves
the benefit of the doubt and assume we can enter it perfectly correctly,
beginning to end, in one go.

Of course, in all programming there are idioms that machine learning should be
able to identify and take advantage of without having to be given a (human
composed) enumeration of language specific rules. For
example, after examining a large body of code, the ML system should know that
require statements often come at the top of most node.js files, that async and
underscore are popular libraries, that typing "var _ " is extremely likely to
be followed by " = require('underscore')", that if we have an anoynmous
function at the end of our async.auto the first line is very likely to be
passing errors back up the callback chain, etc.

Having said that, we may follow a different coding style or we may not use
these libraries but instead use others and the ML system should be able to
take into account those differences and adapt to be efficient for each
programmer.

Training
--------

There is a very large body of open source node.js oriented Javascript code
available through npm (https://www.npmjs.org/). The ML component can be
trained using this code. At first glance, the code can be broken down into two
(overlapping) learning problems, (i) structure, and (ii) identifiers.

The structure of the code is defined by the Abstract Syntax Tree and most
languages have libraries for parsing Javascript. For Python,
https://pypi.python.org/pypi/slimit, is one such library whose end goal is
minifying Javascript but which includes all the component pieces we need.
slimit can give us the abstract syntax tree, lexed tokens, identifiers and
pretty print the snippets that we are going to propose in an auto-complete
situation.

Identifiers reflect on the problem in (at least) two ways:

1. The identifier used to describe a function may, for example, correlate with
the structure of the function, i.e. all the functions implementing my HTTP GET
endpoints may have a name beginning with "get*" vs "post*" for the POST
endpoints and that may inform the structure of the code that follows.

2. Identifiers, obviously, only make sense within their scope. This means that
identifiers corresponding to libraries have universal value whereas
identifiers within modules or blocks are limited to those modules and blocks.
The ML system needs to be able to understand the difference between
"async.auto" and "firstCallback" in our target code.

Features
--------

Given the experimental nature of this project, let's experiment with some
features that we believe will lead to the ML system being able to predict the
code snippet that will follow:

- Language
- Bag of words filename
- Bag of words enclosing function name (if any)
- Bag of words identifiers in scope
- Line number, counting from start & counting from end
- Indent level of the line
- Column of the insert point
- Distance through the file, i.e. line number / total number of lines
- Enclosing context, i.e. the AST we are contained within
- Adjacent context, i.e. the AST preceding and following us in a block (if any)
- The auto-complete prefix, i.e. the user typed 'as' so far
- The tokens preceding the insert point

Predicting identifiers is probably going to be more complex and can perhaps be
broken down into existing identifiers and new identifiers. It should be clear
from the AST whether an identifier is being defined (i.e. is new) or is simply
being used (i.e. must exist already). We should perhaps consider identifiers
as strings of words with word separation typically either being based on a
CamelCase convention or a snake_case convention.

Originating brand new and accurate identifier names is likely to be very
difficult (it's even difficult for human beings, being one of the two hard
things in computer science, along with cache invaliation and off-by-one
errors) but it may be realistic to identify common prefix and/or suffix
patterns. For example, the authors style of programming in the target.js is to
use 'key' and 'keyCallback' consistently in the 'async.auto' construct.
Certainly, we should propose a placeholder identifier and ensure the code
snippets can be efficiently populated by tagging repeated use of the same
identifier within the snippet.

Predicting the subsequent use of a previously defined identifier is a problem
that could benefit greatly from an accurate understanding of the scope of
identifiers but scoping is different from one language to another and we want
to avoid writing a set of language rules. Given that, the ML system should be
given the information it needs to learn how scoping works.

So, what features would make sense for identifier prediction:

- Probably all of the above features for snippet prediction, plus
- "Distance" from the identifier definition measured in terms of AST layers

Testing
-------

Prerequisites
-------------

Sublime Text has 2 auto-complete like capabilities. The first is an 'as-you-
type' pop-up that gives a list of suggested words. Amongst these words there
may be code snippets. While it's easy to quickly see whether a word is the
particular word you want, it's not easy to see if a code snippet is the right
one, and this could be even worse if there are now many variations on a
snippet being automatically generated by an ML system. To truly see whether a
code snippet fits you need to be able to preview that snippet in place. We are
going to need to extend Sublime Text with that capability.

