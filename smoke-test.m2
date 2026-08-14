-- Smoke test for a spack-installed Macaulay2.  Run with
--
--     M2 --script smoke-test.m2
--
-- The point is to check that the interpreter works at all and that the
-- external programs spack installed alongside it can actually be found and
-- run.  It is deliberately quick; it is not a substitute for "M2 --check".

-- the interpreter itself
assert(2^100 == 1267650600228229401496703205376)
R = QQ[x,y,z]
assert(dim ideal(x,y) == 1)
assert(gens gb ideal(x*y, x*z) == matrix {{x*z, x*y}})

-- The external programs, via the packages that wrap them.  Running each
-- package's own tests is the surest way to exercise the program itself, since
-- findProgram raises an error when it is missing and the tests fail when it
-- misbehaves.  (Topcom is a good example: spack builds topcom 1.1.2, which
-- works, while topcom 1.2.0 fails most of these tests.)
scan({
	"CohomCalg",		-- cohomcalg
	"FourTiTwo",		-- 4ti2
	"Msolve",		-- msolve
	"Nauty",		-- nauty
	"Normaliz",		-- normaliz
	"Topcom",		-- topcom
	"gfanInterface"		-- gfan
	}, pkg -> (
	stderr << "-- checking " << pkg << endl;
	check pkg))

-- Polyhedra's own test suite is too big for a smoke test, so just make sure it
-- loads and computes (it uses cddlib and lrslib).
needsPackage "Polyhedra"
assert(numColumns vertices hypercube 3 == 8)

-- csdp, via SemidefiniteProgramming
needsPackage "SemidefiniteProgramming"
S = QQ[u,v,w]
P = sdp({u,v,w}, matrix {{1,u,3-v},{u,5,w},{3-v,w,9+u}}, u+v+w)
(X,y,Z,sdpstatus) = optimize(P, Solver => "CSDP")
assert match("^SDP solved", sdpstatus)

stderr << "-- smoke test passed" << endl
