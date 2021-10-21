const graphql = require('graphql')
const { GraphQLObjectType, GraphQLSchema, GraphQLInt, GraphQLString, GraphQLList } = graphql
//would need to import user data
const UserType = require('./TypeDefs/UserType')

const RootQuery = new GraphQLObjectType({
    name: "RootQueryType",
    fields: {
        getAllUsers: {
            type: new GraphQLList(UserType),
            args: { id: { type: GraphQLInt } },
            resolve(parent, args) {
                return  //SELECT ALL STATEMENT
            }
        }
    }
})

const Mutation = new GraphQLObjectType({
    name: "Mutation",
    fields: {
        createUser: {
            type: UserType,
            args: {
                firstName: { type: GraphQLString },
                lastName: { type: GraphQLString },
                email: { type: GraphQLString },
                password: { type: GraphQLString }
            },
            resolve(parent, args) {
                //args.email
                return args//db.query("INSERT") AND return args is like res.send
            }
        }
    }
})

const schema = new GraphQLSchema({ query: RootQuery, mutation: Mutation })

module.exports = schema