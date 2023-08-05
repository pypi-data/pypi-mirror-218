    ///////////////////////////////////////////////////////////////////////////////
    /// \file extends_funop.hpp
    /// Definitions for extends\<\>::operator()
    //
    //  Copyright 2008 Eric Niebler. Distributed under the Boost
    //  Software License, Version 1.0. (See accompanying file
    //  LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
    template<typename Sig> struct result { typedef typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop< Sig , proto_derived_expr , proto_domain >::type ) >::type const type; };
        BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop0< proto_derived_expr const , proto_domain >::type ) >::type const operator ()() const { typedef boost::proto::result_of::funop0< proto_derived_expr const , proto_domain > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) ) ); } BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop0< proto_derived_expr , proto_domain >::type ) >::type const operator ()() { typedef boost::proto::result_of::funop0< proto_derived_expr , proto_domain > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) ) ); }
        template<typename A0> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop1< proto_derived_expr const , proto_domain , const A0 >::type ) >::type const operator ()(A0 const &a0) const { typedef boost::proto::result_of::funop1< proto_derived_expr const , proto_domain , const A0 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) , a0 ) ); } template<typename A0> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop1< proto_derived_expr , proto_domain , const A0 >::type ) >::type const operator ()(A0 const &a0) { typedef boost::proto::result_of::funop1< proto_derived_expr , proto_domain , const A0 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) , a0 ) ); }
        template<typename A0 , typename A1> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop2< proto_derived_expr const , proto_domain , const A0 , const A1 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1) const { typedef boost::proto::result_of::funop2< proto_derived_expr const , proto_domain , const A0 , const A1 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) , a0 , a1 ) ); } template<typename A0 , typename A1> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop2< proto_derived_expr , proto_domain , const A0 , const A1 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1) { typedef boost::proto::result_of::funop2< proto_derived_expr , proto_domain , const A0 , const A1 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) , a0 , a1 ) ); }
        template<typename A0 , typename A1 , typename A2> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop3< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2) const { typedef boost::proto::result_of::funop3< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) , a0 , a1 , a2 ) ); } template<typename A0 , typename A1 , typename A2> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop3< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2) { typedef boost::proto::result_of::funop3< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) , a0 , a1 , a2 ) ); }
        template<typename A0 , typename A1 , typename A2 , typename A3> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop4< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3) const { typedef boost::proto::result_of::funop4< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) , a0 , a1 , a2 , a3 ) ); } template<typename A0 , typename A1 , typename A2 , typename A3> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop4< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3) { typedef boost::proto::result_of::funop4< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) , a0 , a1 , a2 , a3 ) ); }
        template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop5< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4) const { typedef boost::proto::result_of::funop5< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) , a0 , a1 , a2 , a3 , a4 ) ); } template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop5< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4) { typedef boost::proto::result_of::funop5< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) , a0 , a1 , a2 , a3 , a4 ) ); }
        template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4 , typename A5> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop6< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4 , A5 const &a5) const { typedef boost::proto::result_of::funop6< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) , a0 , a1 , a2 , a3 , a4 , a5 ) ); } template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4 , typename A5> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop6< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4 , A5 const &a5) { typedef boost::proto::result_of::funop6< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) , a0 , a1 , a2 , a3 , a4 , a5 ) ); }
        template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4 , typename A5 , typename A6> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop7< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4 , A5 const &a5 , A6 const &a6) const { typedef boost::proto::result_of::funop7< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) , a0 , a1 , a2 , a3 , a4 , a5 , a6 ) ); } template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4 , typename A5 , typename A6> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop7< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4 , A5 const &a5 , A6 const &a6) { typedef boost::proto::result_of::funop7< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) , a0 , a1 , a2 , a3 , a4 , a5 , a6 ) ); }
        template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4 , typename A5 , typename A6 , typename A7> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop8< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 , const A7 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4 , A5 const &a5 , A6 const &a6 , A7 const &a7) const { typedef boost::proto::result_of::funop8< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 , const A7 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) , a0 , a1 , a2 , a3 , a4 , a5 , a6 , a7 ) ); } template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4 , typename A5 , typename A6 , typename A7> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop8< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 , const A7 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4 , A5 const &a5 , A6 const &a6 , A7 const &a7) { typedef boost::proto::result_of::funop8< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 , const A7 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) , a0 , a1 , a2 , a3 , a4 , a5 , a6 , a7 ) ); }
        template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4 , typename A5 , typename A6 , typename A7 , typename A8> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop9< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 , const A7 , const A8 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4 , A5 const &a5 , A6 const &a6 , A7 const &a7 , A8 const &a8) const { typedef boost::proto::result_of::funop9< proto_derived_expr const , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 , const A7 , const A8 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr const *>(this) , a0 , a1 , a2 , a3 , a4 , a5 , a6 , a7 , a8 ) ); } template<typename A0 , typename A1 , typename A2 , typename A3 , typename A4 , typename A5 , typename A6 , typename A7 , typename A8> BOOST_FORCEINLINE typename BOOST_PROTO_RESULT_OF< proto_generator( typename boost::proto::result_of::funop9< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 , const A7 , const A8 >::type ) >::type const operator ()(A0 const &a0 , A1 const &a1 , A2 const &a2 , A3 const &a3 , A4 const &a4 , A5 const &a5 , A6 const &a6 , A7 const &a7 , A8 const &a8) { typedef boost::proto::result_of::funop9< proto_derived_expr , proto_domain , const A0 , const A1 , const A2 , const A3 , const A4 , const A5 , const A6 , const A7 , const A8 > funop; return proto_generator()( funop::call( *static_cast<proto_derived_expr *>(this) , a0 , a1 , a2 , a3 , a4 , a5 , a6 , a7 , a8 ) ); }
