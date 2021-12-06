export function Title(props) {
    return (
        <div className="h-16 w-full bg-gradient-to-b from-pink-500 to-purple-900 text-4xl text-white flex flex-col justify-center content-center">
            {props.children}
        </div>
    );
}