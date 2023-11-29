parent(bart,homer).
parent(bart,marge).
parent(lisa,homer).
parent(lisa,marge).
parent(maggie,homer).
parent(maggie,marge).
parent(homer,abraham).
parent(herb,abraham).
parent(tod,ned).
parent(rod,ned).
parent(marge,jackie).
parent(patty,jackie).
parent(selma,jackie).
female(maggie).
female(lisa).
female(marge).
female(patty).
female(selma).
female(jackie).
male(bart). 
male(homer).
male(herb).
male(burns).
male(smithers).
male(tod).
male(rod).
male(ned).
male(abraham).
brother(X, Y) :- parent(X, Z), parent(Y, Z), male(X), X \= Y.
sister(X, Y) :- parent(X, Z), parent(Y, Z), female(X), X \= Y.
aunt(X, Y) :- parent(X, Z), sister(Y, Z).
uncle(X, Y) :- parent(X, Z), brother(Y, Z).
grandfather(X, Y) :- parent(X, Z), parent(Z, Y), male(Y).
granddaughter(X, Y) :- parent(Z, X), parent(Y, Z), female(Y).
% Base case: Parent is a direct ancestor
ancestor(X, Y) :- parent(X, Y).

% Recursive case: If Z is an ancestor of Y and X is a parent of Z,
% then X is also an ancestor of Y
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

occupation(joe,oral_surgeon).
occupation(sam,patent_lawyer).
occupation(bill,trial_lawyer).
occupation(cindy,investment_banker).
occupation(joan,civil_lawyer).
occupation(len,plastic_surgeon).
occupation(lance,heart_surgeon).
occupation(frank,brain_surgeon).
occupation(charlie,plastic_surgeon).
occupation(lisa,oral_surgeon).
address(joe,houston).
address(sam,pittsburgh).
address(bill,dallas).
address(cindy,omaha).
address(joan,chicago).
address(len,college_station).
address(lance,los_angeles).
address(frank,dallas).

address(charlie,houston).
address(lisa,san_antonio).
salary(joe,50000).
salary(sam,150000).
salary(bill,200000).
salary(cindy,140000).
salary(joan,80000).
salary(len,70000).
salary(lance,650000).
salary(frank,85000).
salary(charlie,120000).
salary(lisa,190000).

lawyer(X) :- occupation(X, patent_lawyer); occupation(X, trial_lawyer); occupation(X, civil_lawyer).

surgeon(X) :- occupation(X, oral_surgeon); occupation(X, plastic_surgeon); occupation(X, heart_surgeon); occupation(X, brain_surgeon).

query2a(X) :- lawyer(X).
query2b(X) :- surgeon(X), address(X, los_angeles).
query2c(X) :- surgeon(X), address(X, Y), (Y = houston; Y = dallas; Y = san_antonio), salary(X, Z), Z > 100000.


subject(algebra,math).
subject(calculus,math).
subject(dynamics,physics).
subject(electromagnetism,physics).
subject(nuclear,physics).
subject(organic,chemistry).
subject(inorganic,chemistry).
degree(bill,phd,chemistry).
degree(john,bs,math).
degree(chuck,ms,physics).
degree(susan,phd,math).
retired(bill).

canTeach(X, Y) :- 
    degree(X, phd, Z), 
    subject(Y, Z).

canTeach2(X, Y) :- 
    degree(X, phd, Z), 
    subject(Y, Z),
    \+ retired(X).

canTeach3(X, Y) :- 
    degree(X, phd, Z), 
    subject(Y, Z),
    \+ retired(X).

canTeach3(X, Y) :- 
    degree(X, ms, Z), 
    subject(Y, Z),
    \+ retired(X).

bit(0).
bit(1).

octal_code(A, B, C) :- 
    bit(A), 
    bit(B), 
    bit(C),
    format('~w~w~w~n', [A, B, C]).

color(blue).
color(green).
color(red).

mapcolor(WA, NT, SA, Q, NSW, V, T) :-
    color(WA), color(NT), color(SA), color(Q),
    color(NSW), color(V), color(T),
    WA \= NT, WA \= SA,
    NT \= SA, NT \= Q,
    SA \= Q, SA \= NSW, SA \= V,
    Q \= NSW,
    NSW \= V.
